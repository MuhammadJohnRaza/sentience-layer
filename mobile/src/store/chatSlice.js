import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  messages: [
    { id: 'msg_0', isAgent: true, agentName: 'KERNEL', text: 'Multi-agent reasoning active. State your objective.' }
  ],
  isTyping: false,
};

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    addMessage: (state, action) => {
      state.messages.push(action.payload);
    },
    setTypingIndicator: (state, action) => {
      state.isTyping = action.payload;
    },
    clearChatHistory: (state) => {
      state.messages = [
        { id: Date.now().toString(), isAgent: true, agentName: 'KERNEL', text: 'Memory cleared. Ready for new objective.' }
      ];
    }
  }
});

export const { addMessage, setTypingIndicator, clearChatHistory } = chatSlice.actions;
export default chatSlice.reducer;
