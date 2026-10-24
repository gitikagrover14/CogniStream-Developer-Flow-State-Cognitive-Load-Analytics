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
  {
    time: '11:30 AM',
    source: 'GitHub',
    event: 'New commit pushed',
    category: 'Coding',
  },
]

export { activities, sampleEvents }