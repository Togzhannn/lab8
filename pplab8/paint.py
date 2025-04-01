import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Simple Paint")
    clock = pygame.time.Clock()
    
    radius = 5
    drawing_mode = 'line'  # 'line', 'rect', 'circle', 'erase'
    color_mode = 'blue'
    current_color = (0, 0, 255)
    points = []
    start_pos = None  # For rect and circle

    def get_color_from_mode(mode):
        if mode == 'blue':
            return (0, 0, 255)
        elif mode == 'red':
            return (255, 0, 0)
        elif mode == 'green':
            return (0, 255, 0)
        elif mode == 'black':
            return (0, 0, 0)
        return (255, 255, 255)

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
                
                # Color keys
                if event.key == pygame.K_r:
                    color_mode = 'red'
                    current_color = get_color_from_mode(color_mode)
                elif event.key == pygame.K_g:
                    color_mode = 'green'
                    current_color = get_color_from_mode(color_mode)
                elif event.key == pygame.K_b:
                    color_mode = 'blue'
                    current_color = get_color_from_mode(color_mode)
                elif event.key == pygame.K_k:
                    color_mode = 'black'
                    current_color = get_color_from_mode(color_mode)

                # Tool modes
                elif event.key == pygame.K_1:
                    drawing_mode = 'line'
                elif event.key == pygame.K_2:
                    drawing_mode = 'rect'
                elif event.key == pygame.K_3:
                    drawing_mode = 'circle'
                elif event.key == pygame.K_4:
                    drawing_mode = 'erase'
            
            # Size control
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    start_pos = event.pos
                    if drawing_mode == 'line':
                        points.append(event.pos)
                        points = points[-256:]
                elif event.button == 3:  # Right click
                    drawing_mode = 'erase'
                    points.append(event.pos)

            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  # Hold left button to draw
                    if drawing_mode == 'line':
                        position = event.pos
                        points.append(position)
                        points = points[-256:]
                    elif drawing_mode == 'erase':
                        pygame.draw.circle(screen, (0, 0, 0), event.pos, radius)

            if event.type == pygame.MOUSEBUTTONUP:
                end_pos = event.pos
                if drawing_mode in ['rect', 'circle'] and start_pos:
                    if drawing_mode == 'rect':
                        x, y = start_pos
                        w, h = end_pos[0] - x, end_pos[1] - y
                        pygame.draw.rect(screen, current_color, (x, y, w, h), 2)
                    elif drawing_mode == 'circle':
                        radius_circ = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                        pygame.draw.circle(screen, current_color, start_pos, radius_circ, 2)
                start_pos = None

        # Background fill (only if you want to reset)
        # screen.fill((0, 0, 0))  # remove to make persistent drawing

        # Draw lines
        i = 0
        while i < len(points) - 1:
            draw_line_between(screen, i, points[i], points[i + 1], radius, color_mode)
            i += 1

        pygame.display.flip()
        clock.tick(60)

def draw_line_between(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))

    # Determine dynamic color
    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)
    elif color_mode == 'black':
        color = (0, 0, 0)
    else:
        color = (255, 255, 255)

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

main()
