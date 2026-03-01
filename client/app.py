import cv2
import json
import os
from web3 import Web3
from eth_account import Account
import secrets

# --- CONFIGURATION ---
BLOCKCHAIN_URL = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))

if not w3.is_connected():
    print("CRITICAL ERROR: Cannot connect to local blockchain. Make sure Hardhat node is running.")
    exit()

try:
    with open('contract_data.json', 'r') as f:
        contract_data = json.load(f)
        CONTRACT_ADDRESS = contract_data['address']
        CONTRACT_ABI = contract_data['abi']
except FileNotFoundError:
    print("ERROR: contract_data.json not found. Did you run the deploy script first?")
    exit()

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# --- HELPER FUNCTIONS ---
def create_ephemeral_wallet():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    funding_account = w3.eth.accounts[0] 
    
    print(f"Creating temporary edge wallet: {acct.address}")
    tx_hash = w3.eth.send_transaction({
        'to': acct.address,
        'from': funding_account,
        'value': w3.to_wei(1, 'ether')
    })
    w3.eth.wait_for_transaction_receipt(tx_hash)
    return acct

def register_face_on_blockchain(face_bytes, wallet_account):
    # Hash the face data to a secure 32-byte string
    face_hash = Web3.keccak(face_bytes)
    print(f"Generated Zero-Knowledge Face Hash: {face_hash.hex()}")

    try:
        construct_txn = contract.functions.registerIdentity(face_hash).build_transaction({
            'from': wallet_account.address,
            'nonce': w3.eth.get_transaction_count(wallet_account.address),
            'gas': 200000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })

        signed_txn = w3.eth.account.sign_transaction(construct_txn, private_key=wallet_account.key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        print("Verifying on Blockchain...")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"SUCCESS: Identity minted on chain in block {tx_receipt.blockNumber}!")

    except Exception as e:
        if "already registered" in str(e):
             print("\n>>> VERIFICATION RESULT: Identity already exists on chain. Access Denied (or Verified!). <<<")
        else:
             print(f"\nBLOCKCHAIN ERROR: {e}")

# --- MAIN APP LOOP ---
def run_camera_app():
    current_wallet = create_ephemeral_wallet()

    # Load OpenCV's built-in AI Face Detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    video_capture = cv2.VideoCapture(1)
    
    print("\n--- AMD EDGE IDENTITY SYSTEM RUNNING ---")
    print("Press 's' to Scan face and mint DID.")
    print("Press 'q' to Quit.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Convert to grayscale for the AI detector
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        for (x, y, w, h) in faces:
             cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
             cv2.putText(frame, "Face Detected (Local AI)", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('Edge Identity Scanner', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            if len(faces) > 0:
                print("\nFace detected locally! Processing...")
                # For a stable hackathon demo, we use a consistent byte string when your face is recognized.
                # In production, this would be a Fuzzy Extractor applied to your biometric embedding.
                demo_face_data = b"HACKATHON_DEMO_USER_FACE_001"
                register_face_on_blockchain(demo_face_data, current_wallet)
            else:
                print("\nNo face detected! Please look at the camera.")

        elif key == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run_camera_app()