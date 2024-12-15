# Cteker 🌐🚀

**Cteker (Cryptocurrency Transaction Maker)** is a REST API web project built with **Python FastAPI** to send cryptocurrency across multiple blockchain networks.

## Supported Networks 🌉
- **EVM**: ✅
- **TRON**: ✅
- **Solana**: 🔜 (Coming Soon)
- **TON**: 🔜 (50%)

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
   fastapi run
   ```

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