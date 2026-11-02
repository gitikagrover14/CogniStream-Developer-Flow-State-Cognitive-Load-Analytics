import ReactECharts from 'echarts-for-react'

function FocusChart({ option }) {
  return (
    <ReactECharts
      option={option}
      notMerge={true}
      lazyUpdate={true}
      style={{ height: '280px', width: '100%' }}
    />
  )
}

export default FocusChart