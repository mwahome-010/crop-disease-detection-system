
def simulate_prediction():
    """
    Returns sample prediction data for prototype testing.
    This is NOT a real machine-learning prediction.
    """

    return {
        'crop': 'Tomato',
        'plant_part': 'Leaf',
        'disease': 'Early Blight',
        'status': 'Sample disease detection',
        'recommendation': (
            'This is demonstration data. '
            'Crop-specific recommendations will be integrated '
            'with the trained detection system in Stage 2.'
        ),
        'is_simulated': True,
    }
