import pyglet

class main(pyglet.window.Window):
    def __init__(self):
        self.rendering_engine = RenderEngine(self)
        self.world = World(self)

class RenderEngine(pyglet.window.Window):
        def __init__(self, parent):
            super().__init__(caption="test window", width = 1280, height = 720,)
            self.window_center = (self.width // 2, self.height // 2)

            background_image = pyglet.image.load("misc/blueprint-background_HD.png")
            background_image.anchor_x = background_image.width // 2
            background_image.anchor_y = background_image.height // 2

            background_sprite = pyglet.sprite.Sprite(background_image, x=self.window_center[0], y=self.window_center[1],)
            background_sprite.scale = 2

            
            @self.event
            def on_draw():
                self.clear()
                background_sprite.draw()



class World(main):
    def __init__(self, parent):
        self.origin = (0,0)



game = main()
pyglet.app.run()
print("end")