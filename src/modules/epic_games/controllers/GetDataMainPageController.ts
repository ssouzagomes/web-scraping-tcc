import { Request, Response } from 'express'

import { GetDataMainPageService } from '../services/GetDataMainPageService'

export class GetDataMainPageController {
  async handle(request: Request, response: Response): Promise<Response> {
    const getDataMainPageService = new GetDataMainPageService()

    await getDataMainPageService.execute()

    return response.json().status(200)
  }
}