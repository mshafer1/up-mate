import flask
import up_mate_backend

def main():
    up_mate_backend.app.debug = True
    up_mate_backend.app.run(port="5000")


if __name__ == '__main__':
    main()
