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

    % Step 3: Apply Median Filtering for Noise Reduction
    filteredImg = medfilt2(grayImg, [3 3]); % Apply a 3x3 median filter
    steps{end+1} = 'Applied median filtering for noise reduction.';
    imwrite(filteredImg, 'static/results/step_3_filtered.png');
    imagePaths{end+1} = 'static/results/step_3_filtered.png';

    % Step 4: Apply Histogram Equalization
    enhancedImg = histeq(filteredImg); % Enhance the filtered image
    steps{end+1} = 'Applied histogram equalization for contrast enhancement.';
    imwrite(enhancedImg, 'static/results/step_4_enhanced.png');
    imagePaths{end+1} = 'static/results/step_4_enhanced.png';

    % Step 5: Apply Adaptive Thresholding
    binaryImg = imbinarize(enhancedImg, 'adaptive', 'Sensitivity', 0.5);
    steps{end+1} = 'Applied adaptive thresholding.';
    imwrite(binaryImg, 'static/results/step_5_thresholded.png');
    imagePaths{end+1} = 'static/results/step_5_thresholded.png';

    % Step 6: Morphological Operations (Erosion and Dilation)
    se = strel('disk', 2);
    morphImg = imdilate(imerode(binaryImg, se), se); % Erosion followed by Dilation
    steps{end+1} = 'Performed morphological operations (erosion and dilation).';
    imwrite(morphImg, 'static/results/step_6_morphed.png');
    imagePaths{end+1} = 'static/results/step_6_morphed.png';

    % Step 7: Edge Detection with Fine-Tuned Thresholds
    edges = edge(morphImg, 'Canny', [0.1, 0.2]); % Adjusted thresholds
    steps{end+1} = 'Performed edge detection with fine-tuned thresholds.';
    imwrite(edges, 'static/results/step_7_edges.png');
    imagePaths{end+1} = 'static/results/step_7_edges.png';

    % Step 8: Analyze Connected Components
    stats = regionprops(edges, 'BoundingBox', 'Area', 'Centroid');
    steps{end+1} = 'Analyzed connected components for defect detection.';

    % Step 9: Trace through every pixel for defect detection
    % Initialize defect report and counters
    thresholdArea = 1000;
    defectReport = {};
    defectCount = 0;
    annotatedImg = img;
    defectAreas = []; % To store areas for histogram plotting
    
    [rows, cols] = size(edges);  % Get the size of the image
    for i = 1:rows
        for j = 1:cols
            if edges(i, j) == 1 % Check if this pixel is part of the edge
                % Here, we're doing something simple: marking edge pixels red in the annotated image
                annotatedImg(i, j, 1) = 255; % Set red channel to 255 (for red color)
                annotatedImg(i, j, 2) = 0;   % Green and blue to 0 for red
                annotatedImg(i, j, 3) = 0;
                
                % Count this as a defect pixel for reporting (you can modify this logic)
                defectCount = defectCount + 1;
                defectReport{end+1} = sprintf('Edge pixel at (%d, %d)', i, j);
            end
        end
    end

    % Collect defect areas for histogram plotting
    for i = 1:length(stats)
        if stats(i).Area > thresholdArea
            defectAreas = [defectAreas, stats(i).Area]; % Add defect area to the list
        end
    end

    % Plotting the histogram of defect areas
    if ~isempty(defectAreas)
        figure;
        histogram(defectAreas, 20); % Create a histogram with 20 bins
        title('Histogram of Defect Areas');
        xlabel('Defect Area');
        ylabel('Frequency');
        saveas(gcf, 'static/results/defect_area_histogram.png');
        imagePaths{end+1} = 'static/results/defect_area_histogram.png';
    else
        steps{end+1} = 'No large defects found for histogram plotting.';
    end

    % Additional defect reporting if needed
    if defectCount > 0
        annotatedImg = insertText(annotatedImg, [10, 10], 'Defective', 'FontSize', 20, ...
                                  'BoxColor', 'red', 'TextColor', 'white');
        steps{end+1} = 'Annotated defects as "Defective" based on pixel trace.';
    else
        annotatedImg = insertText(annotatedImg, [10, 10], 'OK', 'FontSize', 20, ...
                                  'BoxColor', 'green', 'TextColor', 'white');
        defectReport{end+1} = 'No defects detected.';
        steps{end+1} = 'Annotated image as "OK".';
    end

    % Save final annotated image
    imwrite(annotatedImg, outputPath);
    steps{end+1} = 'Saved the annotated image with pixel-based defect tracing.';
    imagePaths{end+1} = outputPath;
end
