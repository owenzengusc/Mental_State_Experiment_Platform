import pygame
#import pygame.movie

def play_video_with_sound(filename):
    # Initialize pygame
    pygame.init()

    # Load the movie
    movie = pygame.movie.Movie(filename)

    # Set the movie screen size
    screen = pygame.display.set_mode(movie.get_size())

    # Start playing the movie
    movie.play()

    # Main loop to keep the video playing
    while movie.get_busy():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                movie.stop()
                pygame.quit()
                return

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    play_video_with_sound("path_to_your_video.mpg")
