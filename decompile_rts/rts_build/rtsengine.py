# Main

import pygame, my, logic, input, ui, os, math, webbrowser

os.environ['SDL_VIDEO_CENTERED'] = '1'
# preset the mixer init arguments
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.display.set_icon(pygame.image.load('assets/ui/icon.png'))
pygame.init()
pygame.display.set_caption('Aedificus: Dissect')

# Background color start info @ my.py
my.screen.fill(my.PASTELBLUE)
pygame.display.update()

my.gameRunning = my.DEBUGMODE # set to True to skip menus and use default worldgen settings

def run():
	my.input = input.Input()
	menu = MainMenu()
	my.transition = -1 # fade between menus/game states
	if my.gameRunning: # debug mode is enabled
		handler = logic.Handler()
	else:
		pygame.time.wait(600) # pause for effect

	while True: # main game loop

		deltaTime = my.FPSCLOCK.tick(my.FPS)
		if my.gameRunning:
			handler.update(deltaTime / 1000.0) # update the game

		else: # display menu
			nextMenu = menu.update()

			if nextMenu == 'main':
				menu = MainMenu()
				# Start Map Generation
			elif nextMenu == 'embark':
				menu = EmbarkMenu()
				# Shows Credit Page
			elif nextMenu == 'credits':
				menu = CreditsMenu()
				# Quit the Game
			elif nextMenu == 'quit':
				my.input.terminate()
				# Take User to Map Generation Menu
			elif nextMenu == 'play':
				handler = logic.Handler() # start a new game

		if my.transition == 'begin':
			my.transition = 255
		if my.transition > 0:
			my.transition -= 3 * deltaTime / 17
			my.lastSurf.set_alpha(my.transition)
			my.screen.blit(my.lastSurf, (0, 0))

		pygame.display.update()
		# Main Game Title App
		pygame.display.set_caption('Aedificus: Dissect' + ' ' * 10 + 'FPS: ' + str(int(my.FPSCLOCK.get_fps())))


class MainMenu:
	def __init__(self):
		# Image Logo Info
		self.logoImg = pygame.image.load('assets/aedificus title and dude.png').convert_alpha()
		self.logoRect = self.logoImg.get_rect()
		self.logoRect.midtop = (my.HALFWINDOWWIDTH, -773)

		self.versionSurf, self.versionRect = ui.genText('CyborgVillager ' + str(my.VERSIONNUMBER), (0, 0), my.WHITE, ui.BIGFONT)
		self.versionRect.bottomright = (my.WINDOWWIDTH - ui.GAP, my.WINDOWHEIGHT + 20)
# Play & Quit Button Information

		self.playButton = ui.Button(' Play ', 0, (0, 0), 1, 2)
		self.playButton.rect.midtop = (my.HALFWINDOWWIDTH, my.WINDOWHEIGHT)

		self.quitButton = ui.Button(' Quit ', 0, (my.HALFWINDOWWIDTH - 100, my.WINDOWHEIGHT), 1, 1)
		self.creditsButton = ui.Button('Credits', 0, (0, my.WINDOWHEIGHT), 1, 1)
		self.creditsButton.rect.right = my.HALFWINDOWWIDTH + 100

		self.animateOut = False

# Default background info once @ menu
	def update(self):
		my.input.get()
		# background color more info @ my.py
		my.screen.fill(my.PASTELBLUE)

		my.screen.blit(self.logoImg, self.logoRect)
		my.screen.blit(self.versionSurf, self.versionRect)
# Play Button height / location
		if not self.animateOut:
			if self.playButton.rect.y > my.HALFWINDOWHEIGHT + 200:
				# Location Height Y Axis
				self.playButton.rect.y -= math.fabs(my.HALFWINDOWHEIGHT + 300 - self.playButton.rect.y) * 0.1
			if self.quitButton.rect.y > my.HALFWINDOWHEIGHT + 100:
				# Location Height Y Axis
				self.quitButton.rect.y -= math.fabs(my.HALFWINDOWHEIGHT + 380 - self.quitButton.rect.y) * 0.1
				self.creditsButton.rect.y = self.quitButton.rect.y
			if self.logoRect.y < 50:
				self.logoRect.y += math.fabs(30 - self.logoRect.y) * 0.05
			if self.versionRect.bottom > my.WINDOWHEIGHT - ui.GAP:
				self.versionRect.bottom -= math.fabs(my.WINDOWHEIGHT - 5 - self.versionRect.bottom) * 0.1

		elif self.animateOut:
			animateDone = True
			if self.playButton.rect.y < my.WINDOWHEIGHT - 1:
				animateDone = False
				self.playButton.rect.y += (my.WINDOWHEIGHT + 50 - self.playButton.rect.y) * 0.1
			if self.quitButton.rect.y < my.WINDOWHEIGHT - 1:
				animateDone = False
				self.quitButton.rect.y += (my.WINDOWHEIGHT + 50 - self.quitButton.rect.y) * 0.1
				self.creditsButton.rect.y = self.quitButton.rect.y
				self.versionRect.y += 5
			if self.logoRect.y > -750:
				animateDone = False
				self.logoRect.y -= math.fabs(-773 - self.logoRect.y) * 0.1

			if animateDone:
				return self.animateOut

# Input / animation when user has clicked an animaiton "out" will occur as an "exit"
		for button in [self.playButton, self.quitButton, self.creditsButton]:
			button.simulate(my.input)

		if self.playButton.isClicked:
			self.animateOut = 'embark'
		elif self.quitButton.isClicked:
			self.animateOut = 'quit'
		elif self.creditsButton.isClicked:
			self.animateOut = 'credits'


#World Generation Start
class EmbarkMenu:
	"""Customise world generation then embark into a new game"""
	def __init__(self):
		self.sliders = []
		self.sliderData = [{'label': 'Number of mountains', 'valRange': (5 , 25), 'default': 10},
							{'label': 'Number of rivers', 'valRange': (5 , 40), 'default': 20},
							{'label': 'Tree density', 'valRange': (50 , 200), 'default': 125}]
		i = 0
		for data in self.sliderData:
			self.sliders.append(ui.Slider((int(my.WINDOWWIDTH/2 - ui.Slider.size[0]/2), 200 + i*ui.Slider.size[1] + i*ui.GAP),
								 data['valRange'], data['label'], data['default']))
			i += 1

		self.sliderAlpha = 0
		# Return User to Main Menu
		self.backButton = ui.Button(' Back ', 0, (my.HALFWINDOWWIDTH - 100, my.WINDOWHEIGHT), 1, 1)
		# Start the Game
		self.embarkButton = ui.Button('Embark', 0, (my.HALFWINDOWWIDTH + 20, my.WINDOWHEIGHT), 1, 1)
# Image Geneation Loader
		self.logoImg = pygame.image.load('assets/aedificus title smaller.png').convert_alpha()
		self.logoRect = self.logoImg.get_rect()
		self.logoRect.midtop = (my.HALFWINDOWWIDTH, -155)

		self.animateOut = False

# Extra Play Page Information
	def update(self):
		my.input.get()
		my.screen.fill(my.YELLOW)
# Slider Information on "Play" Page for Generation
		for slider in self.sliders:
			if self.sliderAlpha < 255:
				slider.surf.set_alpha(self.sliderAlpha)
				if not self.animateOut:
					self.sliderAlpha += 15
# User World Value Chooser
			value = slider.update()
			if slider.label == 'Number of mountains':
				my.NUMMOUNTAINS = value
			elif slider.label == 'Number of rivers':
				my.NUMRIVERS = value
			elif slider.label == 'Tree density':
				my.TREEFREQUENCY = 200 - value

		self.embarkButton.simulate(my.input)
		if self.embarkButton.isClicked:
			self.animateOut = 'play'
			# Text When User has clicked Embark, shows "generating world" text
			self.loadingSurf, self.loadingRect = ui.genText('GENERATING WORLD', (0,0), my.WHITE, ui.MEGAFONT)
			self.loadingRect.center = (my.HALFWINDOWWIDTH, my.HALFWINDOWHEIGHT)
# Back animation if user clicked on "back" to main page
		self.backButton.simulate(my.input)
		if self.backButton.isClicked:
			self.animateOut = 'main'

		my.screen.blit(self.logoImg, self.logoRect)


		# ANIMATE
		if self.animateOut: # animate out
			animateDone = True
			if self.backButton.rect.y < my.WINDOWHEIGHT - 1:
				animateDone = False
				self.backButton.rect.y += (my.WINDOWHEIGHT + 50 - self.backButton.rect.y) * 0.1
				self.embarkButton.rect.y = self.backButton.rect.y
			if self.logoRect.y > -160:
				animateDone = False
				self.logoRect.y -= math.fabs(-180 - self.logoRect.y) * 0.1
			if self.animateOut == 'play':
				my.screen.fill(my.DARKBLUE, pygame.Rect(self.loadingRect.x - 20, self.loadingRect.y - 20,
														self.loadingRect.width + 40, self.loadingRect.height + 40))
				my.screen.blit(self.loadingSurf, self.loadingRect)
			if self.sliderAlpha > 0:
				self.sliderAlpha -= 15

		else: # animate in
			if self.backButton.rect.y > my.HALFWINDOWWIDTH - 100:
				self.backButton.rect.y -= math.fabs(my.WINDOWHEIGHT * 0.75 - self.backButton.rect.y) * 0.1
				self.embarkButton.rect.y = self.backButton.rect.y

			if self.logoRect.y < 30:
				self.logoRect.y += math.fabs(30 - self.logoRect.y) * 0.1

		if self.animateOut and animateDone:
			if self.animateOut == 'play':
				my.gameRunning = True

				my.transition = 'begin'
				my.lastSurf = my.screen.copy().convert()
				return 'play'
			return 'main'
#World Generation End


# Credits Page Start
class CreditsMenu:
	def __init__(self):
		self.coderImg = pygame.image.load('assets/ui/credits/coder.png').convert_alpha()
		self.coderRect = self.coderImg.get_rect()
		self.coderRect.midbottom = (my.HALFWINDOWWIDTH, 0)

		self.thanksSurf, self.thanksRect = ui.genText('With thanks to Mekire', (0, 0), my.WHITE, ui.BIGFONT)
		self.thanksRect.midtop = (my.HALFWINDOWWIDTH, my.WINDOWHEIGHT)

		self.backButton = ui.Button('Back', 0, (0, 0), 1, 1)
		self.backButton.rect.midtop = (my.HALFWINDOWWIDTH, my.WINDOWHEIGHT)

		self.soundsButton = ui.Button('Sounds courtesy of all these lovely people', 0, (0, 0), 1, 1)
		self.soundsButton.rect.midtop = (my.HALFWINDOWWIDTH, my.WINDOWHEIGHT)
# Credit Button Location @ Credits
		self.ocButton = ui.Button('Special thanks to jellyberg', 0,(0, 0), 1, 1)
		self.ocButton.rect.midtop = (my.HALFWINDOWWIDTH, 455)
		self.animateOut = False

# Credit Page Extra info
	def update(self):
		my.input.get()
		my.screen.fill(my.YELLOW)

		self.backButton.simulate(my.input)
		self.soundsButton.simulate(my.input)
		self.ocButton.simulate(my.input)
		if self.backButton.isClicked:
			self.animateOut = 'main'
		if self.soundsButton.isClicked:
			webbrowser.open('http://www.freesound.org/people/jellyberg/bookmarks/category/27033/', 2)
		if self.ocButton.isClicked:
			webbrowser.open('https://github.com/jellyberg/Aedificus---Fathers_of_Rome', 3)

		my.screen.blit(self.coderImg, self.coderRect)
		my.screen.blit(self.thanksSurf, self.thanksRect)

		if not self.animateOut:
			if self.coderRect.y < 80:
				self.coderRect.y += math.fabs(80 - self.coderRect.y) * 0.05

			if self.backButton.rect.y > my.HALFWINDOWHEIGHT + 100:
				self.backButton.rect.y -= math.fabs(my.HALFWINDOWHEIGHT + 100 - self.backButton.rect.y) * 0.1
			if self.thanksRect.y > my.HALFWINDOWHEIGHT + 60:
				self.thanksRect.y -= math.fabs(my.HALFWINDOWHEIGHT + 50 - self.thanksRect.y) * 0.1
			if self.soundsButton.rect.y > my.HALFWINDOWHEIGHT + 10:
				self.soundsButton.rect.y -= math.fabs(my.HALFWINDOWHEIGHT + 10 - self.soundsButton.rect.y) * 0.1
			if self.ocButton.rect.y > my.HALFWINDOWHEIGHT + 10:
				self.ocButton.rect.y -= math.fabs(my.HALFWINDOWHEIGHT + 10 - self.ocButton.rect.y) * 0.1

		elif self.animateOut:
			animateDone = True
			if self.backButton.rect.y < my.WINDOWHEIGHT - 1:
				animateDone = False
				self.backButton.rect.y += (my.WINDOWHEIGHT + 50 - self.backButton.rect.y) * 0.1
				self.soundsButton.rect.y += (my.WINDOWHEIGHT + 50 - self.soundsButton.rect.y) * 0.1
			if self.coderRect.bottom > 0:
				animateDone = False
				self.coderRect.y -= math.fabs(-400 - self.coderRect.y) * 0.1
			if self.thanksRect.y < my.WINDOWHEIGHT - 1:
				animateDone = False
				self.thanksRect.y += (my.WINDOWHEIGHT + 50 - self.thanksRect.y) * 0.1

		if self.animateOut and animateDone:
			return 'main'
# Credits Page End



if __name__ == '__main__':
	run()