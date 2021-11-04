import { Router } from 'express';
import { epicGamesRouter } from '../modules/epic_games/routes';

const router = Router();

router.use('/epic-games', epicGamesRouter);

export default router;
