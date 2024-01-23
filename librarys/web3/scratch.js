// RPC 연결
const { Web3 } = require('web3');
const rpcUrl = 'https://rpc.ankr.com/polygon';
const web3 = new Web3(rpcUrl); 

// 컨트랙트 인스턴스 생성
const contractAddr = '0xd7d4794c65a8c453459250f56cfd363b5588a2b8';
const tokenId = 4;

const abi = [{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]
const contractInstance = new web3.eth.Contract(abi, contractAddr);

// 데이터 호출 (totalSupply)
// 인자값으로 tokenId 정수값 입력 필요
contractInstance.methods.totalSupply(tokenId).call().then(console.log)