import { useEnsAvatar } from 'wagmi'
import { UseEnsTextsProps, useEnsTexts } from '../hooks/useEnsTexts'
import styles from '@/styles/TextRecords.module.css'

export const TextRecords = ({ name, keys }: UseEnsTextsProps) => {
  const { data: avatar } = useEnsAvatar({ name, chainId: 1 })
  const { data: texts } = useEnsTexts({ name, keys })

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        {avatar && (
          <img
            src={avatar}
            alt={name}
            className={styles.avatar}
          />
        )}
        <span className={styles.name}>{name}</span>
      </div>

      <div className={styles.records}>
        {texts?.map(({ key, value }) => (
          <div key={key} className={styles.record}>
            <span className={styles.key}>{key}</span>
            <span className={styles.value}>{value?.toString() || 'Not set'}</span>
          </div>
        ))}
      </div>
    </div>
  )
} 