import { Router } from 'express'

import { GetDataMainPageController } from '../controllers/GetDataMainPageController'

const epicGamesRouter = Router()

const getDataMainPageController = new GetDataMainPageController()

epicGamesRouter.get('/main-page', getDataMainPageController.handle)

export { epicGamesRouter }