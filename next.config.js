/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: [
      'tokens.1inch.io',
      'tokens-data.1inch.io',
      's2.coinmarketcap.com',
      'cdn.1inch.io'
    ],
  },
}

module.exports = nextConfig 