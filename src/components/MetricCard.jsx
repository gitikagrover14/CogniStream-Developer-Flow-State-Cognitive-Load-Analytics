function MetricCard({ metric }) {
  return (
    <article className="metric-card">
      <div className="metric-top">
        <p className="metric-label">{metric.title}</p>
        <span className="metric-icon">{metric.icon}</span>
      </div>

      <h2>{metric.value}</h2>

      <p className="metric-note">{metric.note}</p>
    </article>
  )
}

export default MetricCard