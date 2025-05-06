import numpy as np
from PIL import Image, ImageDraw

def poisson_disk_maps(width_m=5.4, height_m=7.2,
                      small_r_m=0.05,
                      big_r_m=0.80,
                      min_dist_m=0.40,          # enforce ≈ uniform spacing
                      px_per_m=100,
                      n_images=3,
                      n_circles_range=(15, 20),
                      seed_offset=100,
                      out_prefix="buildings_map_uniform"):
    w_px, h_px = int(width_m * px_per_m), int(height_m * px_per_m)
    r_small_px = max(1, int(small_r_m * px_per_m))
    r_big_px   = max(r_small_px+1, int(big_r_m * px_per_m))
    r_min_px   = int(min_dist_m * px_per_m)

    for idx in range(n_images):
        rng = np.random.default_rng(seed_offset + idx)
        n_target = rng.integers(n_circles_range[0], n_circles_range[1] + 1)

        img = Image.new("1", (w_px, h_px), 1)
        draw = ImageDraw.Draw(img)

        centers = []
        attempts = 0
        max_attempts = 10000

        # Poisson-disk style rejection sampling
        while len(centers) < n_target and attempts < max_attempts:
            attempts += 1
            x = rng.integers(r_big_px, w_px - r_big_px)
            y = rng.integers(r_big_px, h_px - r_big_px)
            if all((x - cx) ** 2 + (y - cy) ** 2 >= r_min_px ** 2 for cx, cy in centers):
                centers.append((x, y))
                # draw solid small circle
                bbox_small = (x - r_small_px, y - r_small_px, x + r_small_px, y + r_small_px)
                draw.ellipse(bbox_small, fill=0)
                # draw dashed big buffer circle
                bbox_big = (x - r_big_px, y - r_big_px, x + r_big_px, y + r_big_px)
                dash_deg, gap_deg = 8, 8
                for ang in range(0, 360, dash_deg + gap_deg):
                    draw.arc(bbox_big, start=ang, end=ang + dash_deg, fill=0, width=1)

        file_name = f"{out_prefix}_{idx+1}_2.png"
        img.save(file_name, dpi=(300, 300))
        print(f"Saved {file_name}  | circles={len(centers)}  attempts={attempts}")

poisson_disk_maps()
