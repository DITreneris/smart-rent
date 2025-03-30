import axios from 'axios';
import { ethers } from 'ethers';
import SmartRentABI from '../contracts/SmartRent.json';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
const CONTRACT_ADDRESS = process.env.REACT_APP_CONTRACT_ADDRESS;

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
}); 