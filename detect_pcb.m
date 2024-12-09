function [defectReport, steps, imagePaths] = detect_pcb(imagePath, outputPath)
    % Initialize step tracker and image paths
    steps = {};
    imagePaths = {};

    % Step 1: Load and preprocess the image
    img = imread(imagePath);
    steps{end+1} = 'Loaded the original image.';
    imwrite(img, 'static/results/step_1_original.png');
    imagePaths{end+1} = 'static/results/step_1_original.png';

    % Step 2: Convert to Grayscale
    grayImg = rgb2gray(img);
    steps{end+1} = 'Converted the image to grayscale.';
    imwrite(grayImg, 'static/results/step_2_grayscale.png');
    imagePaths{end+1} = 'static/results/step_2_grayscale.png';

    % Step 3: Remove Text Markings (e.g., ARDUINO Logo)
    mask = imbinarize(grayImg, 'adaptive');
    mask = imfill(mask, 'holes');
    mask = bwareaopen(mask, 500);
    processedImg = grayImg;
    processedImg(mask) = 255;
    steps{end+1} = 'Removed text markings using thresholding and morphological operations.';
    imwrite(processedImg, 'static/results/step_3_masked.png');
    imagePaths{end+1} = 'static/results/step_3_masked.png';

    % Step 4: Perform Edge Detection
    edges = edge(processedImg, 'Canny');
    steps{end+1} = 'Performed edge detection using the Canny method.';
    imwrite(edges, 'static/results/step_4_edges.png');
    imagePaths{end+1} = 'static/results/step_4_edges.png';

    % Step 5: Analyze Connected Components
    stats = regionprops(edges, 'BoundingBox', 'Area', 'Centroid');
    steps{end+1} = 'Analyzed connected components for defect analysis.';

    % Step 6: Annotate image based on defect detection
    thresholdArea = 1000;
    annotatedImg = img;
    defectReport = {};
    defectCount = 0;

    for i = 1:length(stats)
        if stats(i).Area > thresholdArea
            defectCount = defectCount + 1;
            bbox = stats(i).BoundingBox;
            centroid = stats(i).Centroid;

            % Draw defect rectangle
            annotatedImg = insertShape(annotatedImg, 'Rectangle', bbox, 'Color', 'red', 'LineWidth', 2);
            defectReport{end+1} = sprintf('Defect %d: Area = %.2f, Centroid = (%.2f, %.2f)', ...
                                          defectCount, stats(i).Area, centroid(1), centroid(2));
        end
    end

    if defectCount > 0
        annotatedImg = insertText(annotatedImg, [10, 10], 'Defective', 'FontSize', 20, ...
                                  'BoxColor', 'red', 'TextColor', 'white');
        steps{end+1} = 'Annotated defects as "Defective".';
    else
        annotatedImg = insertText(annotatedImg, [10, 10], 'OK', 'FontSize', 20, ...
                                  'BoxColor', 'green', 'TextColor', 'white');
        defectReport{end+1} = 'No defects detected.';
        steps{end+1} = 'Annotated image as "OK".';
    end

    % Save final annotated image
    imwrite(annotatedImg, outputPath);
    steps{end+1} = 'Saved the annotated image.';
    imagePaths{end+1} = outputPath;
end