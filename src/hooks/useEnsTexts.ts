import { useEnsResolver, useReadContract } from 'wagmi'
import { namehash } from 'viem/ens'

export interface UseEnsTextsProps {
  name: string
  keys: string[]
}

export interface TextRecord {
  key: string
  value: string | null
}

export function useEnsTexts({ name, keys }: UseEnsTextsProps) {
  const { data: resolver } = useEnsResolver({ name })

  const { data: texts } = useReadContract({
    address: resolver?.address,
    abi: [{
      inputs: [
        { name: 'node', type: 'bytes32' },
        { name: 'key', type: 'string' }
      ],
      name: 'text',
      outputs: [{ name: '', type: 'string' }],
      type: 'function'
    }],
    functionName: 'text',
    args: [namehash(name), keys[0]],
    query: {
      enabled: Boolean(resolver?.address && keys.length > 0),
    },
  })

  return {
    data: keys.map((key) => ({
      key,
      value: texts || null,
    })),
  }
} 