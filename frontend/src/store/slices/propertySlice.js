import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { propertyService } from '../../services/api';

// Async thunks
export const fetchProperties = createAsyncThunk(
  'properties/fetchAll',
  async (filters, { rejectWithValue }) => {
    try {
      const response = await propertyService.getProperties(filters);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch properties');
    }
  }
);

export const fetchPropertyById = createAsyncThunk(
  'properties/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      const response = await propertyService.getProperty(id);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch property');
    }
  }
);

export const createProperty = createAsyncThunk(
  'properties/create',
  async (propertyData, { rejectWithValue }) => {
    try {
      const response = await propertyService.createProperty(propertyData);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to create property');
    }
  }
);

export const updateProperty = createAsyncThunk(
  'properties/update',
  async ({ id, propertyData }, { rejectWithValue }) => {
    try {
      const response = await propertyService.updateProperty(id, propertyData);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to update property');
    }
  }
);

export const deleteProperty = createAsyncThunk(
  'properties/delete',
  async (id, { rejectWithValue }) => {
    try {
      await propertyService.deleteProperty(id);
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to delete property');
    }
  }
);

// Initial state
const initialState = {
  properties: [],
  selectedProperty: null,
  loading: false,
  error: null,
  filters: {
    priceMin: '',
    priceMax: '',
    bedrooms: '',
    propertyType: ''
  }
};

// Slice
const propertySlice = createSlice({
  name: 'properties',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    updateFilters: (state, action) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    clearFilters: (state) => {
      state.filters = initialState.filters;
    }
  },
  extraReducers: (builder) => {
    // Fetch all properties
    builder.addCase(fetchProperties.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(fetchProperties.fulfilled, (state, action) => {
      state.loading = false;
      state.properties = action.payload;
    });
    builder.addCase(fetchProperties.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload;
    });

    // Fetch property by ID
    builder.addCase(fetchPropertyById.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(fetchPropertyById.fulfilled, (state, action) => {
      state.loading = false;
      state.selectedProperty = action.payload;
    });
    builder.addCase(fetchPropertyById.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload;
    });

    // Create property
    builder.addCase(createProperty.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(createProperty.fulfilled, (state, action) => {
      state.loading = false;
      state.properties.push(action.payload);
    });
    builder.addCase(createProperty.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload;
    });

    // Update property
    builder.addCase(updateProperty.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(updateProperty.fulfilled, (state, action) => {
      state.loading = false;
      const index = state.properties.findIndex(p => p.id === action.payload.id);
      if (index !== -1) {
        state.properties[index] = action.payload;
      }
      if (state.selectedProperty?.id === action.payload.id) {
        state.selectedProperty = action.payload;
      }
    });
    builder.addCase(updateProperty.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload;
    });

    // Delete property
    builder.addCase(deleteProperty.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(deleteProperty.fulfilled, (state, action) => {
      state.loading = false;
      state.properties = state.properties.filter(p => p.id !== action.payload);
      if (state.selectedProperty?.id === action.payload) {
        state.selectedProperty = null;
      }
    });
    builder.addCase(deleteProperty.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload;
    });
  },
});

export const { clearError, updateFilters, clearFilters } = propertySlice.actions;
export default propertySlice.reducer; 