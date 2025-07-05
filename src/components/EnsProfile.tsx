import { useAccount, useEnsAvatar, useEnsName } from 'wagmi'
import styles from '@/styles/EnsProfile.module.css'

export const EnsProfile = () => {
  const { address } = useAccount()
  const { data: ensName } = useEnsName({ address, chainId: 1 })
  const { data: avatar } = useEnsAvatar({ name: ensName || '', chainId: 1 })

  if (!address) return null

  return (
    <div className={styles.profile}>
      {avatar && (
        <img 
          src={avatar} 
          alt={ensName || address} 
          className={styles.avatar}
        />
      )}
      <div className={styles.info}>
        <span className={styles.name}>{ensName || 'No ENS Name'}</span>
        <span className={styles.address}>
          {address.slice(0, 6)}...{address.slice(-4)}
        </span>
      </div>
    </div>
  )
} 