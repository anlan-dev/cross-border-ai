import type { ResponseCard } from '../types'
import PriceCompareCard from './cards/PriceCompareCard'
import ComplianceCard from './cards/ComplianceCard'
import CopywritingCard from './cards/CopywritingCard'
import StrategyCard from './cards/StrategyCard'
import ProductAnalysisCard from './cards/ProductAnalysisCard'

interface Props {
  card: ResponseCard
}

export default function CardRenderer({ card }: Props) {
  switch (card.type) {
    case 'price_compare':
      return <PriceCompareCard card={card} />
    case 'compliance':
      return <ComplianceCard card={card} />
    case 'copywriting':
      return <CopywritingCard card={card} />
    case 'strategy':
      return <StrategyCard card={card} />
    case 'product_analysis':
      return <ProductAnalysisCard card={card} />
    default:
      return null
  }
}
