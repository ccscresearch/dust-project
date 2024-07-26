import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: 'AIzaSyB-NUMb8uCF7zCl1zYJKQijmdWp1AEKyro',
  authDomain: 'Dust-76a0c.firebaseapp.com',
  projectId: 'Dust-76a0c',
  storageBucket: 'Dust-76a0c.appspot.com',
  messagingSenderId: '394323903489',
  appId: '1:394323903489:web:09a0f56242dccfdf562c00',
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
