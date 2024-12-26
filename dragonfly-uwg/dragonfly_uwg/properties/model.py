# coding=utf-8
"""Model UWG Properties."""
from ..terrain import Terrain
from ..traffic import TrafficPararameter

from dragonfly.extensionutil import model_extension_dicts
from honeybee.typing import float_in_range
from honeybee.altnumber import autocalculate


class ModelUWGProperties(object):
    """UWG Properties for Dragonfly Model.

    Args:
        host: A dragonfly_core Model object that hosts these properties.
        terrain: A Terrain object that dictates the properties of the street and
            ground beneath the buildings. If None, a default terrain object will be
            generated by analysing all of the buildings in the Model and drawing
            a bounding rectangle in the XY plane around them. (Default: None).
        traffic: A TrafficPararameter object that defines the activity and
            intensity of traffic within the urban street canyons. If None,
            traffic intensity will be approximated using the average building
            story count along with a generic traffic schedule. (Default: None).
        tree_coverage_fraction: A number from 0 to 1 that defines the fraction of the
            exposed terrain covered by trees. If Autocalculate, it will be determined
            by evaluating the horizontal area of all ContextShade geometry that has
            a true is_vegetation property. (Default: autocalculate).
        grass_coverage_fraction: A number from 0 to 1 that defines the fraction
            of the exposed terrain that is covered by grass or shrubs.
            Anything not covered in grass is assumed to be pavement. (Default: 0).

    Properties:
        * host
        * terrain
        * traffic
        * tree_coverage_fraction
        * grass_coverage_fraction
        * footprint_density
        * facade_to_site
        * exposed_ground_area
        * is_tree_coverage_autocalcualted
    """

    __slots__ = ('_host', '_terrain', '_traffic', '_tree_coverage_fraction',
                 '_grass_coverage_fraction')

    def __init__(self, host, terrain=None, traffic=None,
                 tree_coverage_fraction=autocalculate, grass_coverage_fraction=0):
        """Initialize Model UWG properties."""
        self._host = host
        self.terrain = terrain
        self.traffic = traffic
        self.tree_coverage_fraction = tree_coverage_fraction
        self.grass_coverage_fraction = grass_coverage_fraction

    @property
    def host(self):
        """Get the Model object hosting these properties."""
        return self._host

    @property
    def terrain(self):
        """Get or set a Terrain object that dictates the properties of the ground."""
        if self._terrain is None:
            return Terrain.from_building_bounding_rect(self.host.buildings)
        return self._terrain

    @terrain.setter
    def terrain(self, value):
        if value is not None:
            assert isinstance(value, Terrain), 'Expected Terrain object for ' \
                'ModelUWGProperties.terrain. Got {}.'.format(type(value))
        self._terrain = value

    @property
    def traffic(self):
        """Get or set a TrafficPararameter object that dictates the street traffic."""
        return self._traffic

    @traffic.setter
    def traffic(self, value):
        if value is not None:
            assert isinstance(value, TrafficPararameter), 'Expected TrafficPararameter' \
                ' object for ModelUWGProperties.traffic. Got {}.'.format(type(value))
        self._traffic = value if value is not None else TrafficPararameter()

    @property
    def tree_coverage_fraction(self):
        """Get or set the fraction of the exposed site area covered in trees."""
        if self._tree_coverage_fraction is None:
            return self._autocalcualted_tree_coverage(self.exposed_ground_area)
        return self._tree_coverage_fraction

    @tree_coverage_fraction.setter
    def tree_coverage_fraction(self, value):
        if value == autocalculate:
            self._tree_coverage_fraction = None
        else:
            self._tree_coverage_fraction = \
                float_in_range(value, 0, 1, 'tree_coverage_fraction')

    @property
    def grass_coverage_fraction(self):
        """Get or set the fraction of the exposed site area covered in grass or shrubs.

        Anything not covered in grass is assumed to be pavement.
        """
        return self._grass_coverage_fraction

    @grass_coverage_fraction.setter
    def grass_coverage_fraction(self, value):
        self._grass_coverage_fraction = \
            float_in_range(value, 0, 1, 'grass_coverage_fraction')

    @property
    def footprint_density(self):
        """Get a fractional number for the footprint density of the model."""
        return self.host.footprint_area / self.terrain.horizontal_area

    @property
    def facade_to_site(self):
        """Get a fractional number for the ratio between the facade are and site area."""
        return self.host.exterior_wall_area / self.terrain.horizontal_area

    @property
    def exposed_ground_area(self):
        """Get the area of the terrain exposed to the outdoor air."""
        return self.terrain.horizontal_area - self.host.footprint_area

    @property
    def is_tree_coverage_autocalcualted(self):
        """Get a boolean for whether tree coverage is autocalcualted from Context."""
        return self._tree_coverage_fraction is None

    def grass_coverage_from_geometry(self, grass_geometry):
        """Set this object's grass_coverage_fraction using an array of Face3Ds.

        Args:
            grass_geometry: An array of Face3Ds that represent grass surfaces.
        """
        grass_area = self.compute_horizontal_area(grass_geometry)
        g_frac = grass_area / self.exposed_ground_area
        self.grass_coverage_fraction = g_frac if g_frac < 1 else 1

    def average_shgc(self, climate_zone):
        """Get the average SHGC across all buildings in the model.

        Args:
            climate_zone: Text for the ASHRAE climate zone, which must include
                the humidity letter (eg. "4A") unless it is climate zone 7 or 8.
        """
        ext_ap_areas = [bldg.exterior_aperture_area for bldg in self.host.buildings]
        total_area = sum(ext_ap_areas)
        try:
            ext_ap_weights = [area / total_area for area in ext_ap_areas]
        except ZeroDivisionError:  # no apertures in model; just use dummy shgc
            return 0.4
        shgc = 0
        for bldg, weight in zip(self.host.buildings, ext_ap_weights):
            if bldg.properties.uwg._shgc is None:
                shgc += bldg.properties.uwg.default_shgc(climate_zone) * weight
            else:
                shgc += bldg.properties.uwg._shgc * weight
        return shgc

    def move(self, moving_vec):
        """Move these properties along a vector.

        Args:
            moving_vec: A ladybug_geometry Vector3D with the direction and distance
                to move the object.
        """
        if self._terrain is not None:
            self._terrain.move(moving_vec)

    def rotate_xy(self, angle, origin):
        """Rotate this Terrain counterclockwise in the XY plane by a certain angle.

        Args:
            angle: An angle in degrees.
            origin: A ladybug_geometry Point3D for the origin around which the
                object will be rotated.
        """
        if self._terrain is not None:
            self._terrain.rotate_xy(angle, origin)

    def reflect(self, plane):
        """Reflect this Terrain across a plane.

        Args:
            plane: A ladybug_geometry Plane across which the object will be reflected.
        """
        if self._terrain is not None:
            self._terrain.reflect(plane)

    def scale(self, factor, origin=None):
        """Scale this Terrain by a factor from an origin point.

        Args:
            factor: A number representing how much the object should be scaled.
            origin: A ladybug_geometry Point3D representing the origin from which
                to scale. If None, it will be scaled from the World origin (0, 0, 0).
        """
        if self._terrain is not None:
            self._terrain.scale(factor, origin)

    def apply_properties_from_dict(self, data):
        """Apply the uwg properties of a dictionary to the host Model of this object.

        Args:
            data: A dictionary representation of an entire dragonfly-core Model.
                Note that this dictionary must have ModelUWGProperties in order
                for this method to successfully apply the uwg properties.
        """
        # check that UWG properties exist and apply the global ones to this object
        assert 'uwg' in data['properties'], \
            'Dictionary possesses no ModelUWGProperties.'
        uwg_data = data['properties']['uwg']
        if 'terrain' in uwg_data and uwg_data['terrain'] is not None:
            self.terrain = Terrain.from_dict(uwg_data['terrain'])
        if 'traffic' in uwg_data and uwg_data['traffic'] is not None:
            self.traffic = TrafficPararameter.from_dict(uwg_data['traffic'])
        if 'tree_coverage_fraction' in uwg_data and \
                uwg_data['tree_coverage_fraction'] != autocalculate.to_dict():
            self.tree_coverage_fraction = uwg_data['tree_coverage_fraction']
        if 'grass_coverage_fraction' in uwg_data:
            self.grass_coverage_fraction = uwg_data['grass_coverage_fraction']

        # collect lists of uwg property dictionaries
        building_u_dicts, _, _, context_u_dicts = \
            model_extension_dicts(data, 'uwg', [], [], [], [])

        # apply uwg properties to objects using the uwg property dictionaries
        for bldg, b_dict in zip(self.host.buildings, building_u_dicts):
            if b_dict is not None:
                bldg.properties.uwg.apply_properties_from_dict(b_dict)
        for shade, s_dict in zip(self.host.context_shades, context_u_dicts):
            if s_dict is not None:
                shade.properties.uwg.apply_properties_from_dict(s_dict)

    def to_dict(self):
        """Return Model UWG properties as a dictionary."""
        base = {'uwg': {'type': 'ModelUWGProperties'}}
        if self._terrain is not None:
            base['uwg']['terrain'] = self._terrain.to_dict()
        base['uwg']['traffic'] = self.traffic.to_dict()
        if self._tree_coverage_fraction is not None:
            base['uwg']['tree_coverage_fraction'] = self.tree_coverage_fraction
        base['uwg']['grass_coverage_fraction'] = self.grass_coverage_fraction
        return base

    def to_uwg_dict(self):
        """Get a dictionary following the input schema of the UWG.

        This dictionary can be serialized into a JSON in order to be run through
        the UWG. Note that this dictionary will only include the properties that
        the dragonfly Model object possesses and will lack all of those provided
        by the UWGSimulationParameter object. For fully simulate-able UWG
        input, the Model.to.uwg method should be used. The keys of the dictionary
        output by this method include the following.

        * bldheight
        * blddensity
        * vertohor
        * grasscover
        * treecover
        * bld
        * h_mix
        * albroof
        * vegroof
        * glzr
        * albwall
        * flr_h
        * charlength
        * albroad
        * droad
        * kroad
        * croad
        * sensanth
        * schtraffic

        """
        # check that the model units are meters before extracting outputs
        assert self.host.units == 'Meters', \
            'Model units must be in Meters to use to_uwg_dict.'

        # get the geometry properties on a per-building level
        floors = [bldg.floor_area for bldg in self.host._buildings]
        footprints = [bldg.footprint_area for bldg in self.host._buildings]
        walls = [bldg.exterior_wall_area for bldg in self.host._buildings]

        total_floor, total_foot, total_wall = sum(floors), sum(footprints), sum(walls)
        floor_weights = [area / total_floor for area in floors]
        foot_weights = [area / total_foot for area in footprints]
        walls_weights = [area / total_wall for area in walls]

        # do some geometry computations with checks
        terrain = self.terrain  # request once to potentially avoid regenerating it
        site_area = terrain.horizontal_area
        density = total_foot / site_area
        assert density <= 1, 'Building footprint areas [{} m2] cannot be larger than ' \
            'the terrain area [{} m2].'.format(total_foot, site_area)
        tree = self._tree_coverage_fraction
        if self._tree_coverage_fraction is None:
            ground_area = site_area - total_foot
            tree = self._autocalcualted_tree_coverage(ground_area)
        tree = tree * (1 - density)  # uwg expcts fraction for whole area
        grass = self.grass_coverage_fraction * (1 - density)  # uwg expcts for whole area
        average_height = self.host.average_height_above_ground
        story_count = self.host.average_story_count_above_ground
        sens_anth = self.traffic._watts_per_area
        if self.traffic._watts_per_area is None:
            sens_anth = self._autocalculated_traffic(story_count)

        # create the dictionary
        base = {'type': 'UWG'}
        base['bldheight'] = average_height
        base['blddensity'] = density if density < 1 else 0.99
        base['vertohor'] = round(sum(walls) / site_area, 5)
        base['treecover'] = round(tree, 5)
        base['grasscover'] = round(grass, 5) if tree + grass + density <= 1 \
            else round(1 - tree - density, 5)
        base['bld'] = self._create_bld_matrix(floor_weights)
        base['h_mix'] = self._weighted_property('fract_heat_to_canyon', floor_weights)
        base['albroof'] = self._weighted_property('roof_albedo', foot_weights)
        base['vegroof'] = self._weighted_property('roof_veg_fraction', foot_weights)
        base['glzr'] = round(self.host.exterior_aperture_area / total_wall, 5)
        base['albwall'] = self._weighted_property('wall_albedo', walls_weights)
        base['flr_h'] = round(average_height / story_count, 5)
        base['charlength'] = round(terrain.characteristic_length, 5)
        base['albroad'] = round(terrain.pavement_albedo, 5)
        base['droad'] = round(terrain.pavement_thickness, 5)
        base['kroad'] = round(terrain.pavement_conductivity, 5)
        base['croad'] = round(terrain.pavement_heat_capacity, 5)
        base['sensanth'] = round(sens_anth, 5)
        base['schtraffic'] = [self.traffic.weekday_schedule,
                              self.traffic.saturday_schedule,
                              self.traffic.sunday_schedule]
        return base

    def duplicate(self, new_host=None):
        """Get a copy of this Model.

        Args:
            new_host: A new Model object that hosts these properties.
                If None, the properties will be duplicated with the same host.
        """
        _host = new_host or self._host
        new_obj = ModelUWGProperties(_host)
        if self._terrain is not None:
            new_obj._terrain = self._terrain.duplicate()
        new_obj._traffic = self._traffic.duplicate()
        new_obj._tree_coverage_fraction = self._tree_coverage_fraction
        new_obj._grass_coverage_fraction = self._grass_coverage_fraction
        return new_obj

    @staticmethod
    def compute_horizontal_area(face3ds):
        """Get the area of a list of Face3D in the XY Plane.

        This is useful for taking geometry representing grass or pavement and
        turning it into a number for grass_coverage_fraction.
        """
        poly2d = Terrain._face3d_to_polygon2d(face3ds)
        return sum([geo.area for geo in poly2d])

    def _create_bld_matrix(self, floor_area_weights):
        """Create the matrix of building programs and vintages for the uwg_dict."""
        bld_dict = {}
        for bldg, weight in zip(self.host._buildings, floor_area_weights):
            uwg_prop = bldg.properties.uwg
            key = '{}_{}'.format(uwg_prop.program, uwg_prop.vintage)
            try:
                bld_dict[key][2] += weight
            except KeyError:  # first time we have this program and vintage
                bld_dict[key] = [uwg_prop.program_uwg, uwg_prop.vintage_uwg, weight]
        # round all weight values to avoid tolerance issues
        for val in bld_dict:
            bld_dict[val][2] = round(bld_dict[val][2], 3)
        return tuple(bld_dict.values())

    def _autocalcualted_tree_coverage(self, ground_area):
        """Autocalculate the tree coverage from the model context shades."""
        veg_shds = []
        for shd in self.host.context_shades:
            if shd.properties.uwg.is_vegetation:
                veg_shds.extend(shd.geometry)
        tree_area = self.compute_horizontal_area(veg_shds)
        if ground_area <= 0:
            return 0
        return tree_area / ground_area if tree_area / ground_area <= 1 else 1

    def _weighted_property(self, attribute, weights):
        weight_val = sum([getattr(bldg.properties.uwg, attribute) * w
                          for bldg, w in zip(self.host._buildings, weights)])
        return round(weight_val, 5)

    @staticmethod
    def _autocalculated_traffic(story_count):
        """Autocalculate the traffic wattage from the average story count."""
        if story_count <= 3:
            return 4
        if story_count <= 6:
            return 10
        return 20

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return 'Model UWG Properties: {}'.format(self.host.identifier)