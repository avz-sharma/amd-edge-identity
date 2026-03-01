# 🛡️ Zero-Knowledge Edge Identity System
**Built for the AMD Slingshot Hackathon: "Human Imagination Built with AI"**

## 📖 Project Overview
Traditional KYC (Know Your Customer) systems force users to upload highly sensitive biometric data to centralized cloud servers, creating massive targets for data breaches. 

This project solves that by creating an **AI-Powered Decentralized Identity System**. It utilizes Edge AI to process biometric data (facial recognition) entirely locally on the user's machine. Instead of transmitting a face to the cloud, it generates a cryptographic Zero-Knowledge hash and mints it to a blockchain Smart Contract as a Decentralized Identifier (DID).

**Zero data leaves the device. Complete identity verification.**

## ✨ Key Features
* **Edge AI Biometrics:** Facial detection runs locally using computer vision, designed to be accelerated by local NPUs (like AMD Ryzen™ AI) for zero-latency privacy.
* **Zero-Knowledge Proofs:** We verify the *presence* of a unique human without storing or transmitting the actual face data.
* **Blockchain Immutability:** Identity hashes are stored on a local Ethereum-compatible network (Hardhat), ensuring identities cannot be tampered with or duplicated.
* **Ephemeral Wallets:** The client automatically generates a secure, localized session wallet to sign identity transactions.

## 🛠️ Tech Stack
* **AI & Computer Vision:** Python, OpenCV (`haarcascades`)
* **Blockchain Layer:** Solidity, Hardhat, Web3.py
* **Hardware Target:** AMD Ryzen™ AI / Local Edge Processors

---

## 🚀 How to Run the Prototype Locally

### Prerequisites
1. [Node.js](https://nodejs.org/) (v18+)
2. [Python](https://www.python.org/) (v3.11+ recommended)

### Step 1: Install Dependencies
Open your terminal in the root project folder and install the blockchain tools:
```bash
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox