from flex.data import FlexObject
from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import List
import logging

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

    def save(self, create_table=True):
        super(Availability, self).save(create_table=create_table)


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
    _avails: List[Availability] = field(default_factory=list)

    @property
    def avails(self) -> List[Availability]:
        avails = self.relation(Availability, backref='asset_id')
        return avails

    @avails.setter
    def avails(self, avails: List[Availability]) -> None:
        for avail in avails:
            avail.bundle_id = self.id
            avail.save()
        self._avails = avails

    def save(self, create_table=True):
        super(Bundle, self).save(create_table=create_table)


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
    playback_features: dict = field(default_factory=dict)
    partner_field: dict = field(default_factory=dict)
    destination_platform: str = ""
    properties: dict = field(default_factory=dict)
    source_stream_provider: str = ""
    asset_version: int = 0
    alid_id: str = ""
    media_source_identifier: str = ""
    media_source_namespace: str = ""
    delivery_partner_id: str = ""
    playback_type: str = PlaybackType.LIVE
    _bundles: List[Bundle] = field(default_factory=list)

    @property
    def bundles(self) -> List[Bundle]:
        bundles = self.relation(Bundle, backref='asset_id')
        return bundles

    @bundles.setter
    def bundles(self, bundles: List[Bundle]) -> None:
        for bundle in bundles:
            bundle.asset_id = self.id
            bundle.save()
        self._bundles = bundles

    def save(self, create_table=True):
        super(Asset, self).save(create_table=create_table)
