import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { contractService } from '../../services/api';

// Async thunks
export const fetchContracts = createAsyncThunk(
  'contracts/fetchAll',
  async (_, { rejectWithValue }) => {
    try {
      const response = await contractService.getContracts();
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch contracts');
    }
  }
);

export const fetchContractById = createAsyncThunk(
  'contracts/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      const response = await contractService.getContract(id);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch contract');
    }
  }
);

export const createContract = createAsyncThunk(
  'contracts/create',
  async (contractData, { rejectWithValue }) => {
    try {
      const response = await contractService.createContract(contractData);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to create contract');
    }
  }
);

export const terminateContract = createAsyncThunk(
  'contracts/terminate',
  async (id, { rejectWithValue }) => {
    try {
      const response = await contractService.terminateContract(id);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to terminate contract');
    }
  }
);

export const completeContract = createAsyncThunk(
  'contracts/complete',
  async (id, { rejectWithValue }) => {
    try {
      const response = await contractService.completeContract(id);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to complete contract');
    }
  }
);

export const payRent = createAsyncThunk(
  'contracts/payRent',
  async ({ id, paymentData }, { rejectWithValue }) => {
    try {
      const response = await contractService.payRent(id, paymentData);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to process rent payment');
    }
  }
);

// Initial state
const initialState = {
  contracts: [],
  selectedContract: null,
  loading: false,
  error: null,
};

// Slice
const contractSlice = createSlice({
  name: 'contracts',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    // Fetch all contracts
    builder.addCase(fetchContracts.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(fetchContracts.fulfilled, (state, action) => {
      state.loading = false;
      state.contracts = action.payload;
    });
    builder.addCase(fetchContracts.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload;
    });

    // Fetch contract by ID
    builder.addCase(fetchContractById.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(fetchContractById.fulfilled, (state, action) => {
      state.loading = false;
      state.selectedContract = action.payload;
    });
    builder.addCase(fetchContractById.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload;
    });

    // Create contract
    builder.addCase(createContract.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(createContract.fulfilled, (state, action) => {
      state.loading = false;
      state.contracts.push(action.payload);
    });
    builder.addCase(createContract.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload;
    });

    // Terminate contract
    builder.addCase(terminateContract.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(terminateContract.fulfilled, (state, action) => {
      state.loading = false;
      const index = state.contracts.findIndex(c => c.id === action.payload.id);
      if (index !== -1) {
        state.contracts[index] = action.payload;
      }
      if (state.selectedContract?.id === action.payload.id) {
        state.selectedContract = action.payload;
      }
    });
    builder.addCase(terminateContract.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload;
    });

    // Complete contract
    builder.addCase(completeContract.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(completeContract.fulfilled, (state, action) => {
      state.loading = false;
      const index = state.contracts.findIndex(c => c.id === action.payload.id);
      if (index !== -1) {
        state.contracts[index] = action.payload;
      }
      if (state.selectedContract?.id === action.payload.id) {
        state.selectedContract = action.payload;
      }
    });
    builder.addCase(completeContract.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload;
    });

    // Pay rent
    builder.addCase(payRent.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(payRent.fulfilled, (state, action) => {
      state.loading = false;
      const index = state.contracts.findIndex(c => c.id === action.payload.id);
      if (index !== -1) {
        state.contracts[index] = action.payload;
      }
      if (state.selectedContract?.id === action.payload.id) {
        state.selectedContract = action.payload;
      }
    });
    builder.addCase(payRent.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload;
    });
  },
});

export const { clearError } = contractSlice.actions;
export default contractSlice.reducer; 