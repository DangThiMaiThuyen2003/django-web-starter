import BaseService from './base'

export class PaymentMethodsService extends BaseService {
  get entity() {
    return 'ecommerce/payment-methods'
  }

  bulkToggle(ids, is_active) {
    return this.request().post(`${this.entity}/bulk-toggle`, { ids, is_active })
  }
}

export default new PaymentMethodsService()


