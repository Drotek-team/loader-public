   def decode_header(self, byte_array: bytearray) -> int:
        magic_nb, dance_size, nb_section = struct.unpack(
            self.FMT_HEADER, byte_array[: struct.calcsize(self.FMT_HEADER)]
        )
        return nb_section

    def decode_section_header(
        self,
        byte_array: bytearray,
        index: int,
    ) -> Tuple[int, int, int]:
        events_id, start, end = struct.unpack(
            self.FMT_SECTION_HEADER,
            byte_array[
                struct.calcsize(self.FMT_HEADER)
                + struct.calcsize(self.FMT_SECTION_HEADER)
                * index : struct.calcsize(self.FMT_HEADER)
                + struct.calcsize(self.FMT_SECTION_HEADER) * (index + 1)
            ],
        )
        return events_id, start, end

    def decode_drone(
        self,
        binary: List[int],
        drone_index: int,
    ) -> Drone:
        drone = Drone(drone_index)
        byte_array = bytearray(binary)
        nb_sections = self.decode_header(byte_array)

        ### These check belong in the procedure, not the object !!!###
        # if magic_nb == self.MAGIC_NB:
        #     decode_report.validation = True
        # if dance_size != len(binary):
        #     decode_report.validation = True

        # if start < end:
        #     decode_report.validation = True
        for index in range(nb_sections):
            (
                events_id,
                events_start_index,
                events_end_index,
            ) = self.decode_section_header(byte_array, index)
            decode_events(
                drone.get_events_by_index(events_id),
                byte_array[events_start_index : events_end_index + 1],
            )
