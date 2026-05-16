import { useDispatch } from 'react-redux';
import { fetchWorkflows } from '../store/workflowSlice';

export const useWorkflow = () => {
  const dispatch = useDispatch();

  const refreshWorkflows = () => {
    dispatch(fetchWorkflows());
  };

  return { refreshWorkflows };
};
