# LNBitcoinGuide
This project tells a story that will help developers and enthusiasts understand how the lightning network funcitons. It uses a python gRPC server to consume a group of LN nodes.
## Requirements
- Download [Polar](https://lightningpolar.com/)
  - If you are having trouble opening the polar app:
    - Go to your Privacy and Security settings on (IOs) and click on Open Anyway.
      ![image](https://github.com/joseblock/LNBitcoinGuide/assets/40869458/24d6371a-65f3-4b87-a2ab-254604943562)

  - Install Docker Desktop
  - Install [Docker-Compose](https://docs.docker.com/desktop/release-notes/)
    - (IOs) To have Docker Compose install a Docker Desktop version before July 2023.
  - Test that Polar UI works
## Import network
- Clone the repo: `git clone`
- In the polar UI click on import network:
  <img width="906" alt="image" src="https://github.com/joseblock/LNBitcoinGuide/assets/40869458/c9f766c8-3f83-4ac1-b659-2dc29461231b">
- Drag the LNBTCGuide.polar.zip file to recreate the network.
- It should look like this:
  <img width="891" alt="image" src="https://github.com/joseblock/LNBitcoinGuide/assets/40869458/1856d727-3903-40c5-af16-c232abfaf513">
- Now you can press the start button.
- In case it didnt work, try building the network by yourself.
## Change source

Go to `/menu.py` and modify the following variables:
  - billetera
  - cafeteria
  - panaderia

Each one of this variables will contain this fields:
  - `"pubkey": '020fe45e80bf106640697d8ae6c7c548f4daebd2281c8e126c81b9f1a95eeb1f98',` 
  - `"cert": '~/.polar/networks/4/volumes/lnd/alice/tls.cert',`
  - `"admin_macaroon": '~/.polar/networks/4/volumes/lnd/alice/data/chain/bitcoin/regtest/admin.macaroon',`
  - `"channel": '127.0.0.1:10001'`

Upadte them as required by comparing the node information in polar:
  <img width="884" alt="image" src="https://github.com/joseblock/LNBitcoinGuide/assets/40869458/f6f0507e-37f0-4017-b244-0a64453eaeb9">
  <img width="1038" alt="image" src="https://github.com/joseblock/LNBitcoinGuide/assets/40869458/fec54fef-93c6-4f11-bfe4-2dba390b7f2a">
## Run the code:
  - `python3 menu.py` 

