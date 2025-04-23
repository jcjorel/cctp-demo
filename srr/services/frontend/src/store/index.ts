import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import bookingsReducer from './slices/bookingsSlice';
import resourcesReducer from './slices/resourcesSlice';
import uiReducer from './slices/uiSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    bookings: bookingsReducer,
    resources: resourcesReducer,
    ui: uiReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore non-serializable values in specified actions
        ignoredActions: ['auth/loginSuccess'],
      },
    }),
});

// Types d'inférence
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
