import { useMemo, useState } from 'react'
import MetricCard from './components/MetricCard'
import ActivityCard from './components/ActivityCard'
import FocusChart from './components/FocusChart'
import './App.css'

const metrics = [
  {
    title: 'Focus Time',
    value: '4h 25m',
    note: 'Illustrative sample data',
    icon: '◷',
  },
  {
    title: 'Interruptions',
    value: '12',
    note: 'Illustrative sample data',
    icon: '↯',
  },
  {
    title: 'Context Switches',
    value: '18',
    note: 'Illustrative sample data',
    icon: '⇄',
  },
  {
    title: 'Activity Sources',
    value: '3',
    note: 'GitHub · Slack · IDE',
    icon: '◈',
  },
]

const activities = [
  {
    name: 'GitHub Activity',
    code: 'GH',
    description: 'Commits, pull requests and repository events.',
    className: 'github',
    status: 'Sample events',
  },
  {
    name: 'Slack Activity',
    code: 'SL',
    description: 'Communication events and potential interruptions.',
    className: 'slack',
    status: 'Sample events',
  },
  {
    name: 'IDE Activity',
    code: 'IDE',
    description: 'Coding events and development activity.',
    className: 'ide',
    status: 'Sample events',
  },
]

const sampleEvents = [
  {
    time: '09:15 AM',
    source: 'GitHub',
    event: 'Commit activity',
    category: 'Coding',
  },
  {
    time: '09:32 AM',
    source: 'IDE',
    event: 'Coding session',
    category: 'Focus',
  },
  {
    time: '10:05 AM',
    source: 'Slack',
    event: 'Message received',
    category: 'Interruption',
  },
  {
    time: '10:20 AM',
    source: 'IDE',
    event: 'Coding session',
    category: 'Focus',
  },
  {
    time: '10:45 AM',
    source: 'GitHub',
    event: 'Pull request activity',
    category: 'Coding',
  },
  {
    time: '11:10 AM',
    source: 'Slack',
    event: 'Message received',
    category: 'Interruption',
  },
]

const chartValues = [42, 65, 50, 78, 58, 88, 70, 46, 74, 60, 83, 55]

const chartTimes = [
  '09:00',
  '09:30',
  '10:00',
  '10:30',
  '11:00',
  '11:30',
  '12:00',
  '12:30',
  '01:00',
  '01:30',
  '02:00',
  '02:30',
]

function App() {
  const [filter, setFilter] = useState('All')

  const filteredEvents = useMemo(() => {
    if (filter === 'All') {
      return sampleEvents
    }

    return sampleEvents.filter((event) => event.source === filter)
  }, [filter])

  const chartOption = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: '#172033',
      borderWidth: 0,
      textStyle: {
        color: '#ffffff',
      },
    },
    grid: {
      left: 12,
      right: 12,
      top: 25,
      bottom: 25,
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: chartTimes,
      axisLine: {
        lineStyle: {
          color: '#e5eaf2',
        },
      },
      axisTick: {
        show: false,
      },
      axisLabel: {
        color: '#8994a7',
      },
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100,
      splitLine: {
        lineStyle: {
          color: '#edf1f7',
          type: 'dashed',
        },
      },
      axisLabel: {
        color: '#8994a7',
        formatter: '{value}%',
      },
    },
    series: [
      {
        name: 'Focus level',
        type: 'line',
        smooth: true,
        data: chartValues,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: {
          width: 3,
          color: '#6878ed',
        },
        itemStyle: {
          color: '#6878ed',
        },
        areaStyle: {
          color: 'rgba(104, 120, 237, 0.12)',
        },
      },
    ],
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <h2 className="brand">
          CogniStream<span>.</span>
        </h2>

        <p className="sidebar-label">WORKSPACE</p>

        <nav className="navigation" aria-label="Main navigation">
          <a className="nav-link active" href="#overview">
            ▦ Overview
          </a>
          <a className="nav-link" href="#flow-state">
            ◷ Flow State
          </a>
          <a className="nav-link" href="#github">
            GH GitHub Activity
          </a>
          <a className="nav-link" href="#slack">
            SL Slack Activity
          </a>
          <a className="nav-link" href="#ide">
            IDE IDE Activity
          </a>
          <a className="nav-link" href="#activity-log">
            ☷ Activity Log
          </a>
        </nav>

        <div className="sidebar-footer">
          <span className="status-dot" />
          UI Preview · Sample Data
        </div>
      </aside>

      <main className="main-content" id="overview">
        <header className="topbar">
          <div>
            <p className="eyebrow">DEVELOPER ANALYTICS</p>
            <h1>Developer Flow Dashboard</h1>
            <p className="subtitle">
              Understand focus, interruptions and development activity.
            </p>
          </div>

          <span className="date-badge">WEEK 1 · UI PREVIEW</span>
        </header>

        <div className="sample-banner" role="status">
          Preview mode: all displayed metrics and chart values are illustrative,
          not real developer telemetry.
        </div>

        <section className="metrics-grid" aria-label="Developer metrics">
          {metrics.map((metric) => (
            <MetricCard key={metric.title} metric={metric} />
          ))}
        </section>

        <section className="content-grid">
          <article className="panel" id="flow-state">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">FLOW ANALYTICS</p>
                <h2>Focus Level Trend</h2>
              </div>

              <span className="tag">Sample Chart</span>
            </div>

            <div className="chart-container">
              <FocusChart option={chartOption} />
            </div>

            <p className="chart-note">
              Illustrative focus scores across sample time intervals.
            </p>
          </article>

          <article className="panel tax-panel">
            <p className="eyebrow">PRODUCTIVITY INSIGHT</p>
            <h2>Context-Switching Tax</h2>

            <div className="insight-icon">⇄</div>

            <p className="placeholder-text">
              This section will estimate focus time lost to interruptions when
              validated telemetry and calculation rules become available.
            </p>

            <span className="tag">Awaiting real data</span>
          </article>
        </section>

        <section className="activity-section" aria-label="Activity sources">
          <div className="section-heading">
            <div>
              <p className="eyebrow">CONNECTED SOURCES</p>
              <h2>Developer Activity</h2>
            </div>

            <span className="tag">3 source types</span>
          </div>

          <div className="activity-grid">
            {activities.map((activity) => (
              <ActivityCard key={activity.name} activity={activity} />
            ))}
          </div>
        </section>

        <section className="panel table-panel" id="activity-log">
          <div className="panel-heading table-heading">
            <div>
              <p className="eyebrow">EVENT MONITOR</p>
              <h2>Recent Activity Log</h2>
            </div>

            <label className="filter-control">
              <span>Filter source</span>

              <select
                value={filter}
                onChange={(event) => setFilter(event.target.value)}
              >
                <option value="All">All</option>
                <option value="GitHub">GitHub</option>
                <option value="Slack">Slack</option>
                <option value="IDE">IDE</option>
              </select>
            </label>
          </div>

          <div className="table-scroll">
            <table>
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Source</th>
                  <th>Event</th>
                  <th>Category</th>
                </tr>
              </thead>

              <tbody>
                {filteredEvents.map((event, index) => (
                  <tr key={`${event.time}-${event.source}-${index}`}>
                    <td>{event.time}</td>
                    <td>
                      <span
                        className={`source-pill ${event.source.toLowerCase()}`}
                      >
                        {event.source}
                      </span>
                    </td>
                    <td>{event.event}</td>
                    <td>{event.category}</td>
                  </tr>
                ))}

                {filteredEvents.length === 0 && (
                  <tr>
                    <td colSpan={4}>No sample events found.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          <p className="chart-note">
            Sample events only · Not connected to live services.
          </p>
        </section>

        <footer className="footer">
          CogniStream · UI Scaffolding · Week 1
        </footer>
      </main>
    </div>
  )
}

export default App