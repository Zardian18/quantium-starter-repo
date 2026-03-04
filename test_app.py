import pytest
from dash import html, dcc
from dash.testing.application_runners import import_app

app = import_app('app')
class TestDashApp:
    def test_header_present(self):
        layout = app.layout
        h1_elements = self._find_components(layout, html.H1)
        assert len(h1_elements)>0, "Header not found in layout"
        header_text = h1_elements[0].children
        assert "Sales Trend" in header_text, f"Expected 'Sales Trend' in header got : {header_text}"
    
    def test_visualization_present(self):
        layout = app.layout
        graph_elements = self._find_components(layout, dcc.Graph)
        assert len(graph_elements)>0, "Graph (dcc.Graph) not found in layout"
        graph_ids =  [g.id for g in graph_elements]
        assert 'sales-graph' in graph_ids, f"Graph with id 'sales-graph' not found. Found {graph_ids}"
    
    def test_region_picker_present(self):
        layout = app.layout
        radio_elements = self._find_components(layout, dcc.RadioItems)
        assert len(radio_elements)>0, "Region picker (radio items) not present"
        radio_ids = [r.id for r in radio_elements]
        assert 'region-selector' in radio_ids, f"Radio Items with id 'region-selector' not found. Found: {radio_ids}"
        radio = radio_elements[0]
        expected_options = ['all', 'north', 'south', 'east', 'west']
        actual_options = [opt['value'] for opt in radio.options]
        for opt in expected_options:
            assert opt in actual_options, f"Option {opt} not found in region picker"
    

    def _find_components(self, component, target_type):
        found = []
        if isinstance(component, target_type):
            found.append(component)
        children = getattr(component, 'children', None)
        if children is None:
            return found
        
        if isinstance(children, list):
            for child in children:
                found.extend(self._find_components(child, target_type))
        else:
            found.extend(self._find_components(children, target_type))
        
        return found
