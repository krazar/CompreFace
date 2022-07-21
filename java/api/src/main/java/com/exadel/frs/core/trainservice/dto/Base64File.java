package com.exadel.frs.core.trainservice.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.annotations.ApiParam;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.NotNull;

import static com.exadel.frs.core.trainservice.system.global.Constants.IMAGE_WITH_ONE_FACE_DESC;

@Data
@NoArgsConstructor
public class Base64File {

    @JsonProperty("file")
    @NotNull
    @ApiParam(value = IMAGE_WITH_ONE_FACE_DESC, required = true)
    private String content;
}
