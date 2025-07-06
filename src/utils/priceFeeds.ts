interface PriceData {
  PRICE: number;
  CHANGEPCT24HOUR: number;
  VOLUME24HOUR: number;
  MKTCAP: number;
}

interface TokenPriceResponse {
  RAW: {
    [key: string]: {
      USD: PriceData;
    };
  };
}

export const fetchTokenPrice = async (symbol: string): Promise<PriceData | null> => {
  try {
    const response = await fetch(
      `https://min-api.cryptocompare.com/data/pricemultifull?fsyms=${symbol}&tsyms=USD`,
      {
        headers: {
          'accept': 'application/json'
        }
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: TokenPriceResponse = await response.json();
    
    if (!data.RAW || !data.RAW[symbol] || !data.RAW[symbol].USD) {
      return null;
    }

    return data.RAW[symbol].USD;
  } catch (error) {
    console.error(`Error fetching price for ${symbol}:`, error);
    return null;
  }
};

export const fetchMultipleTokenPrices = async (symbols: string[]): Promise<{ [key: string]: PriceData | null }> => {
  try {
    const symbolsString = symbols.join(',');
    const response = await fetch(
      `https://min-api.cryptocompare.com/data/pricemultifull?fsyms=${symbolsString}&tsyms=USD`,
      {
        headers: {
          'accept': 'application/json'
        }
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: TokenPriceResponse = await response.json();
    const prices: { [key: string]: PriceData | null } = {};

    for (const symbol of symbols) {
      prices[symbol] = data.RAW?.[symbol]?.USD || null;
    }

    return prices;
  } catch (error) {
    console.error('Error fetching multiple token prices:', error);
    return symbols.reduce((acc, symbol) => ({ ...acc, [symbol]: null }), {});
  }
}; 