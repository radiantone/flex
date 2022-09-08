from flex.data import FlexObject
from dataclasses import dataclass, field


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
