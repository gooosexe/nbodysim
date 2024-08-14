import pygame

# initializations
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# each pixel is one meter

class Body:
	def __init__(self, pos, vel, acc, mass=1):
		self.pos = pos
		self.vel = vel
		self.acc = acc

	def update(self, dt):
		self.vel += self.acc * dt
		self.pos += self.vel * dt

# global variables
bodies = [] # list of bodies
font = pygame.font.SysFont('Arial', 20)
mouseState = 0 # 0 = unpressed, 1 = pressed
curPos = pygame.Vector2(0, 0)
velVec = pygame.Vector2(0, 0)
running = True
dt = 0

def drawText(text, x, y):
	textSurface = font.render(text, False, WHITE)
	screen.blit(textSurface, (x, y))

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			print('mouse down')
			curPos = pygame.mouse.get_pos()
			bodies.append(Body(pygame.Vector2(pygame.mouse.get_pos()), pygame.Vector2(0, 0), pygame.Vector2(0, 0)))
		if event.type == pygame.MOUSEBUTTONUP:
			print('mouse up')
			newPos = pygame.mouse.get_pos()
			bodies[-1].vel = pygame.Vector2(curPos[0] - newPos[0], curPos[1] - newPos[1])
			print(f'vel: {bodies[-1].vel}')

	screen.fill(BLACK)

	for body in bodies:
		body.update(dt)
		pygame.draw.circle(screen, WHITE, body.pos, 10)

	keys = pygame.key.get_pressed()
	mouseState = pygame.mouse.get_pressed()

	if mouseState[0] == 1:
		# get the current mouse position
		newPos = pygame.mouse.get_pos()
		velVec = pygame.Vector2(curPos[0] - newPos[0], curPos[1] - newPos[1])
		pygame.draw.line(screen, WHITE, curPos, pygame.Vector2(curPos[0] + velVec[0], curPos[1] + velVec[1]), 2)
		drawText(str(round(velVec.length(), 2)) + "m/s", 10, 10)

	pygame.display.flip()
	# delta time since last frame
	dt = clock.tick(60) / 1000

pygame.quit()
