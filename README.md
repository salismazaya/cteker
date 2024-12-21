# Cteker 🌐🚀

**Cteker (Cryptocurrency Transaction Maker)** is a REST API web project built with **Python FastAPI** to send cryptocurrency across multiple blockchain networks.

## ⚠️ Danger
**Cteker is currently under development and has not been fully tested. Use at your own risk.**

## Supported Networks 🌉
- **EVM**: ✅
- **TRON**: ✅
- **Solana**: 🔜 (Coming Soon)
- **TON**: ✅
- **Bitcoin**: 🔜 (Coming Soon)
- **Litecoin**: 🔜 (Coming Soon)
- **Dogecoin**: 🔜 (Coming Soon)
- **SUI**: 🔜 (Coming Soon)
- **SEI**: 🔜 (Coming Soon)
---
## Why Use Cteker? 📋
   Cteker provides a robust and efficient way to handle multiple coins and tokens using a unified abstraction layer. Here’s why Cteker is the right choice for your blockchain development needs:

1. Multi-Coin and Multi-Token Support

   Cteker supports a wide range of coins and tokens under the same abstraction, enabling seamless integration and management.

2. Expandable Network and Token Support

   Easily add new networks or tokens using the existing abstraction, making Cteker highly adaptable to your project’s requirements.

3. Automatic Nonce Management

   Cteker automatically handles nonces, ensuring reliable support for multiple simultaneous transactions without manual intervention.

4. Simplified Request Handling

   Just send your request to Cteker, and let it manage the complexities. With Cteker, you can focus on your application logic while we handle the underlying processes.

---

## Requirements 📋
1. **Python 3.10** or newer 🐍
2. **Redis server** 🟥
3. **Git** 🛠️
4. Python libraries specified in `requirements.txt` 📦

---

## Getting Started 🚀

Follow these steps to set up and run the project:

1. **Clone the repository** 🖥️
   ```bash
   git clone https://github.com/salismazaya/cteker
   ```

2. **Copy `.env.example` to `.env`** 📂
   ```bash
   cp .env.example .env
   ```

3. **Fill in `.env` with your values** 🔑

4. **(Optional) Create and activate a virtual environment** 🌱
   Follow [this guide](https://stackoverflow.com/questions/43069780/how-to-create-virtual-env-with-python3) if needed.

5. **Install dependencies** 📦
   ```bash
   pip install -r requirements.txt
   ```

6. **(Optional) Create a New File for Custom Networks**
   You can create a new file at `networks/custom_networks.py` to define custom networks.

   #### Example:

   ```python
   # networks/custom_networks.py
   from core.evm.evm_flexible import EvmFlexible

   networks = [
      EvmFlexible(
         "custom-eth-mainnet", # unique id
         "Ethereum Mainnet", # network name
         "ETH", # network symbol
         "ETHUSDT",  # binance ticker
         "https://eth.drpc.org", # http rpc url
         "https://etherscan.io/tx/" # explorer
      ),
   ]
   ```
   
7. **Run the FastAPI server** ▶️
   ```bash
   granian --interface asgi main:app
   ```

   Granian is a Rust HTTP server for Python applications. You can read more about it [here](https://github.com/emmett-framework/granian).

8. **Access Documentation**  
   Open the documentation in your browser at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

9. 🎉 **Enjoy your API!**

---

## Contact 📬

- **Email**: [salismazaya@gmail.com](mailto:salismazaya@gmail.com)
- **Website**: [https://salism3.dev](https://salism3.dev)
- **Telegram**: [@salismftah](https://t.me/salismftah)

---

Happy coding! 💻✨