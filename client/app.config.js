module.exports = {
  apps : [{
    name: 'spotify-stats',
    script: 'npm',
    args: 'run serve',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'development',
      PORT: 3050,
      HOST: '0.0.0.0'
    },
    env_production: {
      NODE_ENV: 'production',
      PORT: 3050,
      HOST: '0.0.0.0'
    }
  }],
};
