/**
 * Sentience Layer - Node.js API Gateway
 * Acts as a reverse proxy and real-time gateway for the Python backend
 */

import express, { Express, Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import dotenv from 'dotenv';
import { createServer } from 'http';
import { Server } from 'socket.io';
import pino from 'pino';
import axios from 'axios';

dotenv.config();

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
});

const app: Express = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: process.env.CORS_ORIGIN || '*',
    methods: ['GET', 'POST'],
  },
});

const PORT = process.env.NODE_PORT || 4000;
const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:8000';

// Middleware
app.use(helmet());
app.use(cors());
app.use(compression());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Request logging
app.use((req: Request, res: Response, next: NextFunction) => {
  const start = Date.now();
  logger.info({ method: req.method, path: req.path }, 'Request started');
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    logger.info({ 
      method: req.method, 
      path: req.path, 
      status: res.statusCode, 
      duration 
    }, 'Request completed');
  });
  
  next();
});

// Health check
app.get('/health', (req: Request, res: Response) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '4.0.0',
    service: 'node-gateway'
  });
});

// Proxy to Python API
app.all('/api/*', async (req: Request, res: Response) => {
  try {
    const path = req.originalUrl.replace('/api/', '');
    const url = `${PYTHON_API_URL}/api/v1/${path}`;
    
    const response = await axios({
      method: req.method,
      url,
      data: req.body,
      headers: {
        ...req.headers,
        host: new URL(PYTHON_API_URL).host,
      },
      params: req.query,
    });
    
    res.status(response.status).json(response.data);
  } catch (error: any) {
    logger.error({ error: error.message }, 'Proxy error');
    res.status(error.response?.status || 500).json({
      error: 'Proxy error',
      message: error.message,
    });
  }
});

// WebSocket connection handling
io.on('connection', (socket) => {
  logger.info({ socketId: socket.id }, 'WebSocket client connected');
  
  // Forward messages to Python backend
  socket.on('message', async (data) => {
    try {
      const response = await axios.post(`${PYTHON_API_URL}/api/v1/ws/message`, {
        socket_id: socket.id,
        data,
      });
      socket.emit('response', response.data);
    } catch (error: any) {
      logger.error({ error: error.message }, 'WebSocket message error');
      socket.emit('error', { message: error.message });
    }
  });
  
  // Handle subscription to specific channels
  socket.on('subscribe', (channel: string) => {
    socket.join(channel);
    logger.info({ socketId: socket.id, channel }, 'Subscribed to channel');
  });
  
  socket.on('unsubscribe', (channel: string) => {
    socket.leave(channel);
    logger.info({ socketId: socket.id, channel }, 'Unsubscribed from channel');
  });
  
  socket.on('disconnect', () => {
    logger.info({ socketId: socket.id }, 'WebSocket client disconnected');
  });
});

// Error handling middleware
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  logger.error({ error: err.message, stack: err.stack }, 'Unhandled error');
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong',
  });
});

// Start server
httpServer.listen(PORT, () => {
  logger.info({ port: PORT }, 'Node.js gateway started');
});

export { app, io, httpServer };