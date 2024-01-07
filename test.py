from detect import run
results = run(weights='modelss/best_11.pt', source='/workspaces/fish-cube-api/temp_image.jpg')
print(results[0][1])