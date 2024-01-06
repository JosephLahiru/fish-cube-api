from detect import run
results = run(weights='modelss/best.pt', source='test_images/test1.jpg')
print(results)