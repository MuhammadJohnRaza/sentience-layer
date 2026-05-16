import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

export const fetchWorkflows = createAsyncThunk(
  'workflow/fetchAll',
  async () => {
    // Mocking API call
    return [
      {
        id: '1',
        title: 'Neural Optimization',
        description: 'Optimizing kernel weights for enhanced causal inference.',
        status: 'completed',
        progress: 100,
        agentCount: 12,
        duration: '45s',
        actions: 142
      },
      {
        id: '2',
        title: 'Market Analysis',
        description: 'Scanning global sentiment for product-market fit.',
        status: 'processing',
        progress: 64,
        agentCount: 8,
        duration: '2m',
        actions: 89
      }
    ];
  }
);

const workflowSlice = createSlice({
  name: 'workflow',
  initialState: {
    workflows: [],
    inputs: [],
    loading: false,
    error: null
  },
  reducers: {
    addInput: (state, action) => {
      state.inputs.push(action.payload);
    },
    updateWorkflow: (state, action) => {
      const index = state.workflows.findIndex(w => w.id === action.payload.id);
      if (index !== -1) {
        state.workflows[index] = { ...state.workflows[index], ...action.payload };
      }
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchWorkflows.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchWorkflows.fulfilled, (state, action) => {
        state.loading = false;
        state.workflows = action.payload;
      })
      .addCase(fetchWorkflows.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  }
});

export const { addInput, updateWorkflow } = workflowSlice.actions;
export default workflowSlice.reducer;
