import service, { requestWithRetry } from './index'

export const listConnectors = (vertical = null) =>
  service.get('/api/connectors', { params: vertical ? { vertical } : {} })

export const healthCheckAll = () =>
  service.get('/api/connectors/health')

export const fetchConnector = (name, params = {}) =>
  requestWithRetry(() => service.post(`/api/connectors/${name}/fetch`, params), 2, 1500)
