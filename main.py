from common.response import Response

from lib.blueprint import Blueprint
from lib.router import Router
from common.request import Request


def main():
    router = Router(5555)

    @router.get("/hello/:oren")
    def handle(req: Request, res: Response):
        res.status(431).send({'params': req.params['oren']})

    @router.post("/hello/:od")
    def ha(req: Request, res: Response):
        res.status(434).send(req.body)

    stam_router = Blueprint("/stam")

    @stam_router.get("/qqq")
    def stam(req: Request, res: Response):
        res.status(204).send("Blueprint result")

    router.register_blueprint(stam_router)

    router.run()


if __name__ == "__main__":
    main()
