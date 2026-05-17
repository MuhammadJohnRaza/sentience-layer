/**
 * Formats a raw bytes number into a human-readable string (e.g. 1.2 MB)
 */
export const formatBytes = (bytes, decimals = 2) => {
  if (!+bytes) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
};

/**
 * Delays execution for a given amount of milliseconds (useful for simulating network/processing delays)
 */
export const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Truncates a string to a given length and appends an ellipsis
 */
export const truncateText = (text, maxLength = 50) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};

/**
 * Generates a pseudo-random hex ID (useful for mock actions/nodes)
 */
export const generateNodeId = () => {
  return Math.random().toString(16).slice(2, 10);
};

/**
 * Parses a standard timestamp into a readable [HH:MM:SS] format
 */
export const formatTelemetryTime = (timestamp = Date.now()) => {
  const date = new Date(timestamp);
  const pad = (n) => n.toString().padStart(2, '0');
  return `[${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}]`;
};
