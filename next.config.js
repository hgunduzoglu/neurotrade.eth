/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['assets.coingecko.com'],
  },
  env: {
    MORALIS_API_KEY: process.env.MORALIS_API_KEY,
  },
}

module.exports = nextConfig 