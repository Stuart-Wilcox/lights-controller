import servepy
import src.Server.handlers

app = servepy.App()
router = servepy.Router()

router.get('/', handlers.get_light_state)
router.post('/', handlers.set_light_state)

app.use(router)

app.listen(port=8080, hostname='10.88.111.30')
