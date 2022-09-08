"""
 id: int(11) NN auto_increment = 149537934
        created_at: datetime(6) NN
        updated_at: datetime(6) NN
        playback_type: varchar(255) NN
        source_ther_id: int(11)
        source_live_start: datetime(6)
        source_live_end: datetime(6)
        duration: bigint(20)
        entity_id: char(32) NN
        end_credits_time: varchar(64) NN
        deleted_at: datetime(6) NN
        channel_id: char(32)
        source_stormflow_id: varchar(255) NN
        version: bigint(20) NN
        playback_features: json
        partner_field: json
        destination_platform: varchar(255)
        properties: json
        source_stream_provider: varchar(255)
        asset_version: int(11) NN default 1
        alid_id: binary(16)
        media_source_identifier: varchar(255)
        media_source_namespace: varchar(255)
        delivery_partner_id: varchar(255)

catalog_bundle: table
    + columns
        id: int(11) NN auto_increment = 189309392
        created_at: datetime(6) NN
        updated_at: datetime(6) NN
        type: varchar(45) NN
        package_id: int(11)
        released_at: datetime(6)
        deleted_at: datetime(6) NN
        asset_id: int(11) NN
        allow_start_over: tinyint(1) NN
        cp_id: int(11)
        playable_state: varchar(255)
        nfl_mobile_limiter: tinyint(1) NN
        version: bigint(20) NN
        allow_offline: tinyint(1) NN default 0
        max_resolution: varchar(32)
        max_dynamic_range: varchar(32)
        avail_id: binary(16)
        allow_co_viewing: tinyint(1) NN default 0
        distribution_context: varchar(32)
        min_promotional_start: datetime(6)
        content_entitlement: varchar(255)
        properties: json
        brand_id: char(32)
    + indices
        catalog_bundle_asset_id_58ff358c: index (asset_id, type, package_id, deleted_at) type btree
        catalog_bundle_asset_id_bb310140: index (asset_id) type btree
        catalog_bundle_playable_state_495f878b_uniq: index (playable_state) type btree
        catalog_bundle_avail_id_43cc5202: index (avail_id) type btree
    + keys
        #1: PK (id)
    + foreign-keys
        catalog_bundle_asset_id_bb310140_fk_catalog_asset_id: foreign key (asset_id) -> catalog_asset (id)


catalog_availability: table
    + columns
        id: int(11) NN auto_increment = 604154009
        created_at: datetime(6) NN
        updated_at: datetime(6) NN
        device_id: int(11) NN
        available_datetime: datetime(6) NN
        expires_datetime: datetime(6)
        geo_right_type: varchar(255)
        geo_value_type: varchar(255)
        geo_value: varchar(255)
        bundle_id: int(11) NN
        geok_da_id: varchar(255) NN
        available_finalized: tinyint(1) NN
        expires_finalized: tinyint(1) NN
        device_location_sharing: json
    + indices
        catalog_availability_available_datetime_adcbac91_idx: index (available_datetime, updated_at, bundle_id) type btree
        catalog_availability_available_datetime_fe649b0d_uniq: index (available_datetime) type btree
        catalog_availability_expires_datetime_f2df494c_uniq: index (expires_datetime) type btree
        catalog_availability_0533a258: index (bundle_id) type btree
        catalog_availability_geok_da_id_0f3cc84a_uniq: index (geok_da_id) type btree
        catalog_availability_available_finalized_5a423b53_uniq: index (available_finalized) type btree
        catalog_availability_expires_finalized_5f7ee81c_uniq: index (expires_finalized) type btree
"""
from flex.data import FlexObject
from dataclasses import field
from pydantic.dataclasses import dataclass


@dataclass
class Bundle(FlexObject):

    created_at: int = 0
    updated_at: int = 0

    type: str = ""
    package_id: str = ""
    released_at: int = 0
    deleted_at: int = 0
    asset_id: str = ""
    allow_start_over: bool = False
    cp_id: int = 0
    playable_state: str = ""
    nfl_mobile_limiter: bool = False
    version: int = 0
    allow_offline: bool = False
    max_resolution: str = ""
    max_dynamic_range: str = ""
    allow_co_viewing: bool = False
    distribution_context: str = ""
    min_promotional_start: int = 0
    content_entitlement: str = ""
    properties: dict = field(default_factory=dict)
    brand: str = ""
    _avails = []

    @property
    def availabilities(self) -> []:
        avails = self.relation(Availability, backref='bundle_id')
        return avails

    @availabilities.setter
    def availabilities(self, avails: []) -> None:
        for avail in avails:
            avail.bundle_id = self.id

        self._avails = avails

    def save(self, create_table=True):
        super(Bundle, self).save(create_table=create_table)

        for avail in self._avails:
            avail.save()

@dataclass
class Availability(FlexObject):

    created_at: int = 0
    updated_at: int = 0
    device_id: int = -1
    available_datetime: int = 0
    expires_datetime: int = 0
    geo_right_type: str = ""
    geo_value_type: str = ""
    geo_value: str = ""
    bundle_id: str = ""
    geok_da_id: str = ""
    available_finalized: bool = False
    expires_finalized: bool = False
    device_location_sharing: dict = field(default_factory=dict)


@dataclass
class Asset(FlexObject):

    class PlaybackType:
        LIVE = "LIVE"
        LOOPBACK = "LOOPBACK"

    created_at: int = 0
    updated_at: int = 0
    source_ther_id: int = 0
    source_live_start: int = 0
    source_live_end: int = 0
    duration: int = 0
    entity_id: str = ""
    end_credits_time: str = ""
    deleted_at: int = 0
    channel_id: str = ""
    source_stormflow_id: str = ""
    version: int = 0
    _playback_features: dict = field(default_factory=dict)
    _partner_field: dict = field(default_factory=dict)
    destination_platform: str = ""
    _properties: dict = None
    source_stream_provider: str = ""
    asset_version: int = 0
    alid_id: str = ""
    media_source_identifier: str = ""
    media_source_namespace: str = ""
    delivery_partner_id: str = ""
    playback_type: str = PlaybackType.LIVE
    _bundles = []

    @property
    def bundles(self) -> []:
        bundles = self.relation(Bundle, backref='asset_id')
        return bundles

    @bundles.setter
    def bundles(self, bundles: []) -> None:
        for bundle in bundles:
            bundle.asset_id = self.id

        self._bundles = bundles

    @property
    def playback_features(self) -> dict:
        return self._playback_features

    @playback_features.setter
    def playback_features(self, playback_features: dict) -> None:
        self._playback_features = playback_features

    @property
    def partner_field(self) -> dict:
        return self._playback_features

    @partner_field.setter
    def partner_field(self, partner_field: dict) -> None:
        self._partner_field = partner_field

    @property
    def properties(self) -> dict:
        return self._playback_features

    @properties.setter
    def properties(self, properties: dict) -> None:
        self._properties = properties

    def save(self, create_table=True):
        super(Asset, self).save(create_table=create_table)

        for bundle in self._bundles:
            bundle.save()
