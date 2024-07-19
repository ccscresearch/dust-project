import React, { createContext, useEffect, useState } from 'react';
import { User } from 'firebase/auth';

interface AuthContextData {
  user: User | null;
  isAuthenticated: boolean;
  setUser: React.Dispatch<React.SetStateAction<User | null>>;
  isUsingAggregatedDatabase: boolean;
  setIsUsingAggregatedDatabase: React.Dispatch<React.SetStateAction<boolean>>;
}

export const AuthContext = createContext<AuthContextData>({
  user: null,
  isAuthenticated: false,
  setUser: () => {},
  isUsingAggregatedDatabase: false,
  setIsUsingAggregatedDatabase: () => {},
});

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isUsingAggregatedDatabase, setIsUsingAggregatedDatabase] =
    useState(false);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
      setIsAuthenticated(true);
    }
  }, []);

  useEffect(() => {
    if (user) {
      localStorage.setItem('user', JSON.stringify(user));
      setIsAuthenticated(true);
    } else {
      localStorage.removeItem('user');
      setIsAuthenticated(false);
    }
  }, [user]);

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated,
        setUser,
        isUsingAggregatedDatabase,
        setIsUsingAggregatedDatabase,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
