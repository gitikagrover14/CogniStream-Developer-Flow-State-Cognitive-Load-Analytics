function ActivityCard({ activity }) {
  return (
    <article className="panel activity-card" id={activity.className}>
      <div className={`activity-icon ${activity.className}`}>
        {activity.code}
      </div>

      <div className="activity-info">
        <h3>{activity.name}</h3>
        <p>{activity.description}</p>
        <span className="tag">{activity.status}</span>
      </div>
    </article>
  )
}

export default ActivityCard